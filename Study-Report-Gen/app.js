document.addEventListener('DOMContentLoaded', () => {
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    let audioBlob = null;

    const startRecordButton = document.getElementById('startRecord');
    const stopRecordButton = document.getElementById('stopRecord');
    const recordingStatus = document.getElementById('recording-status');
    const languageSelect = document.getElementById('language-select');
    const transcriptionText = document.getElementById('transcription-text');
    const generateStudyButton = document.getElementById('generate-study');
    const studyDocument = document.getElementById('study-document');
    const downloadStudyButton = document.getElementById('download-study');
    const audioFileInput = document.getElementById('audio-file-input');
    const audioPlayer = document.getElementById('audio-player');

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.continuous = true;
    recognition.interimResults = true;

    const transcriptionProgress = document.getElementById('transcription-progress');
    let totalTranscriptionLength = 0;

    recognition.onresult = (event) => {
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
                totalTranscriptionLength += transcript.length;
                const progress = Math.min((totalTranscriptionLength / 500) * 100, 100);
                transcriptionProgress.style.width = `${progress}%`;
            }
        }
        if (finalTranscript) {
            transcriptionText.value += finalTranscript;
            generateStudyButton.disabled = false;
        }
    };

    recognition.onerror = (event) => {
        console.error('Error en el reconocimiento:', event.error);
        stopRecording();
    };

    languageSelect.addEventListener('change', () => {
        recognition.lang = languageSelect.value;
    });

    startRecordButton.addEventListener('click', startRecording);
    stopRecordButton.addEventListener('click', stopRecording);
    generateStudyButton.addEventListener('click', generateStudyDocument);
    downloadStudyButton.addEventListener('click', downloadStudy);

    function startRecording() {
        if (isRecording) return;

        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream, {
                    mimeType: 'audio/webm'
                });
                audioChunks = [];

                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        audioChunks.push(event.data);
                    }
                };

                mediaRecorder.onstop = () => {
                    audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    audioPlayer.src = audioUrl;
                    audioPlayer.style.display = 'block';
                };

                mediaRecorder.start(1000);
                recognition.start();
                isRecording = true;

                startRecordButton.disabled = true;
                stopRecordButton.disabled = false;
                recordingStatus.textContent = 'Grabando...';
                recordingStatus.style.color = '#e53e3e';
            })
            .catch(error => {
                console.error('Error al acceder al micrófono:', error);
                alert('No se pudo acceder al micrófono. Por favor, verifica los permisos.');
            });
    }

    function stopRecording() {
        if (!isRecording) return;

        mediaRecorder.stop();
        recognition.stop();
        isRecording = false;

        mediaRecorder.stream.getTracks().forEach(track => track.stop());

        startRecordButton.disabled = false;
        stopRecordButton.disabled = true;
        recordingStatus.textContent = 'No grabando';
        recordingStatus.style.color = 'initial';
    }

    async function generateStudyDocument() {
        const text = transcriptionText.value.trim();
        if (!text) return;

        generateStudyButton.disabled = true;
        studyDocument.innerHTML = '<p>Generando documento de estudio...</p>';

        try {
            const response = await fetch('generate_study.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    language: languageSelect.value
                })
            });

            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Error en la respuesta del servidor');
            }

            if (data.error) {
                throw new Error(data.error);
            }

            studyDocument.innerHTML = formatStudyDocument(data.content);
            downloadStudyButton.disabled = false;

        } catch (error) {
            console.error('Error al generar el documento:', error);
            studyDocument.innerHTML = `<p class="error">Error: ${error.message}</p>`;
            downloadStudyButton.disabled = true;
        } finally {
            generateStudyButton.disabled = false;
        }
    }

    function formatStudyDocument(content) {
        return content.split('\n').map(line => {
            if (line.startsWith('#')) {
                return `<h3>${line.substring(1).trim()}</h3>`;
            } else if (line.startsWith('-')) {
                return `<li>${line.substring(1).trim()}</li>`;
            } else if (line.trim() === '') {
                return '<br>';
            } else {
                return `<p>${line}</p>`;
            }
        }).join('');
    }

    function downloadStudy() {
        const content = studyDocument.innerHTML;
        const blob = new Blob([`
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Documento de Estudio</title>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }
                    h3 { color: #2b6cb0; }
                    li { margin-bottom: 10px; }
                </style>
            </head>
            <body>${content}</body>
            </html>
        `], { type: 'text/html' });

        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'documento_estudio.html';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    audioFileInput.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const allowedTypes = ['audio/mp3', 'audio/wav', 'audio/flac', 'audio/mpeg'];
        if (!allowedTypes.includes(file.type)) {
            alert('Por favor, sube un archivo de audio en formato MP3, WAV o FLAC');
            return;
        }

        // Mostrar estado de procesamiento
        studyDocument.innerHTML = '<p>Procesando archivo de audio...</p>';
        transcriptionText.value = '';

        const reader = new FileReader();
        reader.onload = async (e) => {
            try {
                // Configurar el reproductor de audio
                audioPlayer.src = URL.createObjectURL(file);
                audioPlayer.style.display = 'block';

                // Configurar el reconocimiento de voz
                recognition.lang = languageSelect.value;
                recognition.continuous = true;
                recognition.interimResults = true;

                // Crear contexto de audio
                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const audioBuffer = await audioContext.decodeAudioData(e.target.result);
                
                // Crear nodo de fuente de audio y conectarlo al destino
                const source = audioContext.createBufferSource();
                source.buffer = audioBuffer;
                source.connect(audioContext.destination);

                // Configurar el reproductor de audio para la transcripción
                audioPlayer.onplay = () => {
                    try {
                        recognition.start();
                        studyDocument.innerHTML = '<p>Transcribiendo audio...</p>';
                    } catch (error) {
                        console.error('Error al iniciar el reconocimiento:', error);
                    }
                };

                audioPlayer.onpause = () => {
                    try {
                        recognition.stop();
                    } catch (error) {
                        console.error('Error al detener el reconocimiento:', error);
                    }
                };

                audioPlayer.onended = () => {
                    try {
                        recognition.stop();
                        generateStudyButton.disabled = false;
                        studyDocument.innerHTML = '<p>Transcripción completada</p>';
                    } catch (error) {
                        console.error('Error al finalizar el reconocimiento:', error);
                    }
                };

                // Manejar errores de reconocimiento
                recognition.onerror = (error) => {
                    console.error('Error en el reconocimiento:', error);
                    studyDocument.innerHTML = '<p class="error">Error en la transcripción: ' + error.error + '</p>';
                };

                // Limpiar transcripción anterior
                transcriptionText.value = '';
                generateStudyButton.disabled = true;

            } catch (error) {
                console.error('Error al procesar el audio:', error);
                studyDocument.innerHTML = '<p class="error">Error al procesar el archivo de audio</p>';
                alert('Error al procesar el archivo de audio. Por favor, intenta con otro archivo.');
            }
        };

        reader.onerror = (error) => {
            console.error('Error al leer el archivo:', error);
            studyDocument.innerHTML = '<p class="error">Error al leer el archivo</p>';
        };

        reader.readAsArrayBuffer(file);
    });
});