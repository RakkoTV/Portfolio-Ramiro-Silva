document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    body.style.margin = '0';
    body.style.padding = '20px';
    body.style.fontFamily = '"Inter", sans-serif';
    body.style.backgroundColor = '#f5f5f5';

    const mainContainer = document.createElement('div');
    mainContainer.style.display = 'flex';
    mainContainer.style.maxWidth = '100%';
    mainContainer.style.height = 'calc(100vh - 40px)';
    mainContainer.style.margin = '0 auto';
    mainContainer.style.gap = '20px';

    const foldersContainer = document.createElement('div');
    foldersContainer.style.flex = '0 0 300px';
    foldersContainer.style.padding = '20px';
    foldersContainer.style.backgroundColor = '#ffffff';
    foldersContainer.style.borderRadius = '8px';
    foldersContainer.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
    foldersContainer.style.overflowY = 'auto';

    const title = document.createElement('h1');
    title.textContent = 'Explorador de Carpetas';
    title.style.marginBottom = '20px';
    title.style.color = '#333';
    title.style.fontSize = '1.5rem';

    const folderList = document.createElement('div');
    folderList.style.display = 'flex';
    folderList.style.flexDirection = 'column';
    folderList.style.gap = '10px';

    const previewContainer = document.createElement('div');
    previewContainer.style.flex = '1';
    previewContainer.style.backgroundColor = '#ffffff';
    previewContainer.style.borderRadius = '8px';
    previewContainer.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
    previewContainer.style.overflow = 'hidden';
    previewContainer.style.position = 'relative';

    foldersContainer.appendChild(title);
    foldersContainer.appendChild(folderList);
    mainContainer.appendChild(foldersContainer);
    mainContainer.appendChild(previewContainer);
    body.appendChild(mainContainer);

    // Función para crear un elemento de carpeta
    function createFolderItem(folderName) {
        const item = document.createElement('div');
        item.style.padding = '10px 15px';
        item.style.backgroundColor = '#f8f9fa';
        item.style.borderRadius = '6px';
        item.style.cursor = 'pointer';
        item.style.transition = 'all 0.2s';
        item.style.display = 'flex';
        item.style.alignItems = 'center';
        item.style.gap = '10px';

        const icon = document.createElement('div');
        icon.innerHTML = '📁';
        icon.style.fontSize = '20px';

        const name = document.createElement('div');
        name.textContent = folderName;
        name.style.fontWeight = '500';
        name.style.color = '#444';
        name.style.flex = '1';

        item.appendChild(icon);
        item.appendChild(name);

        item.addEventListener('mouseover', () => {
            item.style.backgroundColor = '#e9ecef';
        });

        item.addEventListener('mouseout', () => {
            item.style.backgroundColor = '#f8f9fa';
        });

        item.addEventListener('click', () => {
            loadPreview(folderName);
            // Resaltar la carpeta seleccionada
            document.querySelectorAll('.folder-item').forEach(el => {
                el.style.backgroundColor = '#f8f9fa';
                el.classList.remove('selected');
            });
            item.style.backgroundColor = '#e9ecef';
            item.classList.add('selected');
        });

        item.classList.add('folder-item');
        return item;
    }

    // Función para cargar la vista previa
    function loadPreview(folderName) {
        const iframe = document.createElement('iframe');
        iframe.style.width = '100%';
        iframe.style.height = '100%';
        iframe.style.border = 'none';
        iframe.src = `${folderName}/index.html`;

        previewContainer.innerHTML = '';
        previewContainer.appendChild(iframe);
    }

    // Proyectos principales actualizados
    const projectFolders = [
        'ImpactAds-Landing',
        'Video-Downloader-Pro',
        'Wordle-Uruguayo',
        'Modern-UI-Template',
        'Memory-Game-Pro',
        'v0-Dashboard-Metrics',
        'SocialManager-SaaS',
        'Multi-Chat-Aggregator',
        'PTJ-PDF-to-JPEG',
        'Media-3D-Gallery',
        'Vet-Booking-System',
        'Study-Report-Gen',
        'Meta-Generator-TS'
    ];

    projectFolders.forEach(folderName => {
        const item = createFolderItem(folderName);
        folderList.appendChild(item);
    });

    // Seleccionar la primera carpeta por defecto
    const firstFolder = document.querySelector('.folder-item');
    if (firstFolder) {
        firstFolder.click();
    }
});