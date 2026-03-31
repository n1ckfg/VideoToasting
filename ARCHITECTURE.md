# VideoToasting Architecture

Recreation of NewTek Video Toaster (1990s) video transition effects using modern web technologies.

## Tech Stack
- **p5.js 1.9.0** - Canvas rendering and WebGL abstraction
- **GLSL** - Fragment shaders for GPU-accelerated effects
- **Vanilla HTML/JS** - No build system, runs directly in browser

## Project Structure

```
VideoToasting/
├── index.html           # Effect catalog with status indicators
├── AGENTS.md            # Agent instructions for effect generation
├── run.bat / run.command # Local server launchers
├── ref/                 # Reference documentation (ignored)
└── [effect].html        # Individual effect implementations (14 total)
```

## Effect File Pattern

Each effect is a standalone HTML file with this structure:

1. **Vertex Shader** - Passes texture coordinates to fragment shader
2. **Fragment Shader** - Implements the visual effect using:
   - `uTime` - Animation progress (frameCount * 0.016)
   - `uResolution` - Canvas dimensions
   - `vTexCoord` - Normalized UV coordinates (0-1)
3. **p5.js Setup** - Creates WebGL canvas and shader
4. **p5.js Draw Loop** - Updates uniforms and renders

## Effects Catalog

| Effect | Description |
|--------|-------------|
| blinds | Vertical slats compress/expand |
| push-pull | Source enters from sides |
| split | Video divided in two pieces |
| squeeze-zoom | Shrink/expand equally |
| swap | Pieces cross each other |
| trails | Motion leaves afterimages |
| trajectory | Squeezed video flies around |
| transporter | Star Trek-style beam effect |
| tumble | Flips around axis |
| neon-bands | Palette color cycling |
| camera-iris | Expanding/contracting iris |
| bear | Shape-masked wipe |
| giraffe | Anti-aliased animated wipe |
| blinds-3-expand | 3-column rectangle effect |

## p5.js Shader Pattern

Each effect uses this p5.js WEBGL shader pattern:

```javascript
// Vertex shader: use p5.js transformation matrices
const vertexShader = `
    attribute vec3 aPosition;
    attribute vec2 aTexCoord;
    uniform mat4 uModelViewMatrix;
    uniform mat4 uProjectionMatrix;
    varying vec2 vTexCoord;
    void main() {
        vTexCoord = aTexCoord;
        gl_Position = uProjectionMatrix * uModelViewMatrix * vec4(aPosition, 1.0);
    }
`;

// Setup: WEBGL mode required
function setup() {
    createCanvas(windowWidth, windowHeight, WEBGL);
    noStroke();
    shaderProgram = createShader(vertexShader, fragmentShader);
}

// Draw: activate shader, set uniforms, render plane
function draw() {
    shader(shaderProgram);
    shaderProgram.setUniform('uTime', frameCount * 0.016);
    shaderProgram.setUniform('uResolution', [width, height]);
    plane(width, height);
}
```

GLSL notes:
- Use `#define` for loop bounds (WebGL requires constant expressions)
- Use `vec3` for colors, not `vec2`
- Avoid `== 0.0` float comparisons; use `< 0.5` instead
