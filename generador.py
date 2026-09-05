import os
import glob
import google.generativeai as genai

# Conectar con tu llave secreta
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# Esta configuración asegura que expresiones como $x^2 + y^2$ se rendericen correctamente
mathjax_config = """
<script>
  MathJax = { tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] } };
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
"""

# Busca todos los borradores de texto
for archivo_txt in glob.glob("borradores/*.txt"):
    with open(archivo_txt, "r", encoding="utf-8") as f:
        contenido = f.read()
    
    # Las instrucciones para la IA
    prompt = f"""
    Eres un desarrollador web experto. Convierte este borrador de una clase de matemáticas en un archivo HTML completo, semántico y atractivo. 
    Usa MathJax para las fórmulas. Devuelve SOLO el código HTML.
    
    Borrador de la clase:
    {contenido}
    """
    
    # Generar la página web
    respuesta = model.generate_content(prompt)
    html = respuesta.text.strip().removeprefix("```html").removesuffix("```")
    
    # Insertar la configuración matemática en el HTML
    if "</head>" in html:
        html = html.replace("</head>", mathjax_config + "\n</head>")
    
    # Guardar el nuevo archivo HTML
    nombre_base = os.path.basename(archivo_txt).replace(".txt", ".html")
    with open(nombre_base, "w", encoding="utf-8") as f:
        f.write(html)
