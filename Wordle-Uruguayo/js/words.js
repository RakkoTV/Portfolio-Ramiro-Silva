// Base de datos de palabras uruguayas para Wordle
// Formato: Array de objetos con palabra y definición

const palabrasUruguayas = [
  {
    palabra: "BONDI",
    definicion: "Autobús o transporte público colectivo."
  },
  {
    palabra: "BUZO",
    definicion: "Suéter o jersey, prenda de vestir abrigada."
  },
  {
    palabra: "GURI",
    definicion: "Niño o chico pequeño, término cariñoso para referirse a los niños."
  },
  {
    palabra: "MATE",
    definicion: "Bebida tradicional uruguaya hecha con yerba mate."
  },
  {
    palabra: "TERMO",
    definicion: "Recipiente para mantener caliente el agua para el mate."
  },
  {
    palabra: "BOLSO",
    definicion: "Hincha del Club Nacional de Football."
  },
  {
    palabra: "MANYA",
    definicion: "Hincha del Club Atlético Peñarol."
  },
  {
    palabra: "CHETO",
    definicion: "Persona elegante o de clase alta, a veces usado despectivamente."
  },
  {
    palabra: "BOINA",
    definicion: "Sombrero típico usado tradicionalmente en Uruguay."
  },
  {
    palabra: "BOTON",
    definicion: "Policía o agente de la ley, término coloquial."
  },
  {
    palabra: "FAINA",
    definicion: "Comida típica que acompaña a la pizza, hecha de harina de garbanzos."
  },
  {
    palabra: "LONJA",
    definicion: "Tienda o comercio, especialmente de productos alimenticios."
  },
  {
    palabra: "CHIVA",
    definicion: "Mentira o información falsa."
  },
  {
    palabra: "PILON",
    definicion: "Regalo extra o adicional que se da al comprar algo."
  },
  {
    palabra: "TACHO",
    definicion: "Basurero o recipiente para la basura."
  },
  {
    palabra: "TINTO",
    definicion: "Vino tinto, bebida alcohólica muy popular."
  },
  {
    palabra: "YERBA",
    definicion: "Hierba utilizada para preparar el mate."
  },
  {
    palabra: "PLATA",
    definicion: "Dinero o efectivo."
  },
  {
    palabra: "PIQUE",
    definicion: "Rivalidad o competencia, especialmente en deportes."
  },
  {
    palabra: "ASADO",
    definicion: "Barbacoa o carne a la parrilla, plato nacional uruguayo."
  },
  {
    palabra: "DULCE",
    definicion: "Postre típico, especialmente el dulce de leche."
  },
  {
    palabra: "TORTA",
    definicion: "Pastel o tarta, postre horneado."
  },
  {
    palabra: "FRUTA",
    definicion: "Pronunciado con acento uruguayo, producto comestible de ciertas plantas."
  },
  {
    palabra: "SALAO",
    definicion: "Forma corta de 'salado', significa difícil o asombroso."
  },
  {
    palabra: "NOCHE",
    definicion: "Período entre el atardecer y el amanecer, con pronunciación uruguaya."
  },
  {
    palabra: "VICHA",
    definicion: "Forma conjugada de 'vichar', que significa curiosear o mirar."
  },
  {
    palabra: "MANGO",
    definicion: "Dinero, especialmente referido a una unidad monetaria."
  },
  {
    palabra: "JODER",
    definicion: "Molestar o fastidiar a alguien."
  },
  {
    palabra: "JOYA",
    definicion: "Excelente o muy bueno, expresión de aprobación."
  },
  {
    palabra: "LOCO",
    definicion: "Amigo o compañero, forma coloquial de dirigirse a alguien."
  },
  {
    palabra: "NABO",
    definicion: "Persona tonta o despistada, insulto suave."
  },
  {
    palabra: "PILA",
    definicion: "Mucho o en gran cantidad."
  },
  {
    palabra: "PRONTO",
    definicion: "Listo o preparado para algo."
  },
  {
    palabra: "TRUCHO",
    definicion: "Falso o de mala calidad."
  },
  {
    palabra: "ZAFAR",
    definicion: "Escapar o librarse de una situación complicada."
  },
  {
    palabra: "ZANJA",
    definicion: "Bebida alcohólica barata o de baja calidad."
  },
  {
    palabra: "VAMOS",
    definicion: "Expresión de ánimo, típicamente dicha como '¡Vamo' arriba!'"
  },
  {
    palabra: "GURISES",
    definicion: "Niños o chicos, plural de 'gurí'."
  },
  {
    palabra: "BOTIJA",
    definicion: "Niño o chico pequeño, similar a 'gurí'."
  },
  {
    palabra: "DEMÁS",
    definicion: "Muy bueno o excelente, expresión de aprobación."
  }
];

// Palabras de 5 letras para el juego Wordle
const palabrasWordle = palabrasUruguayas.filter(item => item.palabra.length === 5);

// Exportar las palabras para su uso en el juego
export { palabrasWordle, palabrasUruguayas };
