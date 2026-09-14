import os
import re

DIR = '/Users/nick/GitHub/VideoToasting/effects'

COLOR_MAP = {
    r'vec3\(1\.0,\s*0\.3,\s*0\.3\)': 'texRed',
    r'vec3\(0\.8,\s*0\.3,\s*0\.3\)': 'texRed',
    
    r'vec3\(0\.3,\s*0\.3,\s*1\.0\)': 'texBlue',
    r'vec3\(0\.0,\s*0\.5,\s*1\.0\)': 'texBlue',
    
    r'vec3\(1\.0,\s*0\.5,\s*0\.0\)': 'texOrange',
    r'vec3\(1\.0,\s*0\.6,\s*0\.2\)': 'texOrange',
    
    r'vec3\(0\.3,\s*1\.0,\s*0\.3\)': 'texGreen',
    r'vec3\(0\.2,\s*0\.6,\s*0\.2\)': 'texGreen',
    r'vec3\(0\.0,\s*1\.0,\s*0\.8\)': 'texGreen',
    
    r'vec3\(1\.0,\s*1\.0,\s*0\.3\)': 'texYellow',
    r'vec3\(1\.0,\s*1\.0,\s*0\.0\)': 'texYellow',
    r'vec3\(1\.0,\s*0\.8,\s*0\.4\)': 'texYellow',
    r'vec3\(1\.0,\s*0\.8,\s*0\.2\)': 'texYellow',
    
    r'vec3\(0\.8,\s*0\.8,\s*0\.8\)': 'texGray'
}

UNIFORM_DECLARATIONS = """
            uniform sampler2D texRed;
            uniform sampler2D texBlue;
            uniform sampler2D texOrange;
            uniform sampler2D texGreen;
            uniform sampler2D texYellow;
            uniform sampler2D texGray;
"""

SETUP_ADDITIONS = """
            vidRed = createVideo(['../images/bedtime.mp4']);
            vidRed.hide(); vidRed.loop(); vidRed.volume(0);
            vidBlue = createVideo(['../images/best_friend.mp4']);
            vidBlue.hide(); vidBlue.loop(); vidBlue.volume(0);
            vidOrange = createVideo(['../images/nope_camel.mp4']);
            vidOrange.hide(); vidOrange.loop(); vidOrange.volume(0);
            vidGreen = createVideo(['../images/oblueterate.mp4']);
            vidGreen.hide(); vidGreen.loop(); vidGreen.volume(0);
            vidYellow = createVideo(['../images/sinistar.mp4']);
            vidYellow.hide(); vidYellow.loop(); vidYellow.volume(0);
            vidGray = createVideo(['../images/snow_shiba.mp4']);
            vidGray.hide(); vidGray.loop(); vidGray.volume(0);
"""

DRAW_ADDITIONS = """
            shaderProgram.setUniform('texRed', vidRed);
            shaderProgram.setUniform('texBlue', vidBlue);
            shaderProgram.setUniform('texOrange', vidOrange);
            shaderProgram.setUniform('texGreen', vidGreen);
            shaderProgram.setUniform('texYellow', vidYellow);
            shaderProgram.setUniform('texGray', vidGray);
"""

for f in os.listdir(DIR):
    if not f.endswith('.html'): continue
    path = os.path.join(DIR, f)
    with open(path, 'r') as file:
        content = file.read()
    
    # 1. Add global variables for videos
    if 'let shaderProgram;' in content:
        content = content.replace('let shaderProgram;', 'let shaderProgram;\n        let vidRed, vidBlue, vidOrange, vidGreen, vidYellow, vidGray;')
        
    # 2. Add uniforms to fragment shader
    if 'uniform vec2 uResolution;' in content:
        content = content.replace('uniform vec2 uResolution;', 'uniform vec2 uResolution;' + UNIFORM_DECLARATIONS)
        
    # 3. Add setup additions
    if 'shaderProgram = createShader(vertexShader, fragmentShader);' in content:
        content = content.replace('shaderProgram = createShader(vertexShader, fragmentShader);', 
                                  'shaderProgram = createShader(vertexShader, fragmentShader);\n' + SETUP_ADDITIONS)
                                  
    # 4. Add draw additions
    if 'shaderProgram.setUniform(\'uResolution\', [width, height]);' in content:
        content = content.replace('shaderProgram.setUniform(\'uResolution\', [width, height]);',
                                  'shaderProgram.setUniform(\'uResolution\', [width, height]);\n' + DRAW_ADDITIONS)

    # Determine coordinate variable
    coord_var = 'uv' if 'vec2 uv =' in content else 'vTexCoord'
    # Wait, in squeeze-zoom, uv is declared. But we should make sure uv is the right one!
    # Let's replace colors
    for pattern, tex_name in COLOR_MAP.items():
        # Using a regex to replace color with texture2D(texName, coord).rgb
        # But wait, in trails.html, there is "uv = vTexCoord;" or something? We'll use coord_var.
        # But if the replacement needs to be more robust:
        def replacer(match):
            return f"texture2D({tex_name}, {coord_var}).rgb"
        content = re.sub(pattern, replacer, content)

    with open(path, 'w') as file:
        file.write(content)

print("Processed all files.")
