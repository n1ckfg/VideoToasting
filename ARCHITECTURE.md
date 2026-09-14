# VideoToasting Architecture

## Overview

VideoToasting is a web-based implementation of classic 1990s NewTek Video Toaster visual effects, recreated using modern WebGL technologies (p5.js and GLSL shaders). The project demonstrates how analog-era broadcast video effects can be reimplemented in a browser environment.

## Technology Stack

- **Frontend Framework**: p5.js (WebGL mode)
- **Shader Language**: GLSL (OpenGL Shading Language)
- **Rendering**: WebGL 2D/3D canvas rendering
- **File Format**: Individual HTML files with embedded JavaScript and GLSL shaders

## Architecture Components

### 1. File Structure

```
VideoToasting/
├── index.html                    # Main navigation/status page
├── effects/                      # Individual effect implementations
│   └── <effect-name>.html
├── ref/
│   └── video_toaster_methods.md # Reference documentation
├── docs/                         # Project documentation (e.g. PLAN.md)
├── images/                       # Generated images or references
└── run.command / run.bat        # Platform-specific launchers
```

### 2. Standard Effect Template

Each effect follows a consistent architectural pattern:

```
HTML Container
├── p5.js Library (CDN)
├── Vertex Shader (GLSL)
│   └── Standard quad setup with UV coordinates
├── Fragment Shader (GLSL)
│   ├── Effect-specific computation
│   ├── Uniform inputs: uTime, uResolution
│   └── Varying inputs: vTexCoord
└── p5.js Application Code
    ├── setup(): Initialize canvas and shader
    ├── draw(): Animation loop updating uniforms
    └── windowResized(): Responsive handling
```

### 3. Shader Architecture

#### Vertex Shader (Standard)
```glsl
attribute vec2 aPosition;     // Corner positions (-1 to 1)
attribute vec2 aTexCoord;     // UV coordinates (0 to 1)
varying vec2 vTexCoord;       // Passed to fragment shader

void main() {
    vTexCoord = aTexCoord;
    gl_Position = vec4(aPosition, 0, 1);
}
```

#### Fragment Shader Pattern
```glsl
precision mediump float;           // Precision for mobile devices
varying vec2 vTexCoord;            // UV coordinates
uniform float uTime;               // Animation time
uniform vec2 uResolution;          // Canvas resolution

void main() {
    // Effect-specific GLSL computation
    gl_FragColor = vec4(color, alpha);
}
```

### 4. Effect Categories

The Video Toaster effects fall into several implementation categories:

#### A. Geometric Transform Effects
These manipulate spatial coordinates and UV mapping:
- **Blinds**: Vertical slats compressing/expanding
- **Push/Pull**: Side-entering transitions
- **Split**: Screen division effects
- **Squeeze/Zoom**: Uniform scaling transforms
- **Swap**: Cross-moving segments
- **Trajectory**: Flying motion with squeeze
- **Tumble**: Axis-based flipping

#### B. Temporal/Motion Effects
These use time-based computations and motion vectors:
- **Trails**: Motion blur/trail effects
- **Transporter**: Motion detection with beam overlay

#### C. Palette/Color Effects
These simulate the original hardware's palette manipulation:
- **NEON BANDS**: Color cycling with horizontal bands
- **CAMERA IRIS**: 4-color animated iris expansion/contraction
- **BEAR**: Animated wipe with matte color outline
- **GIRAFFE**: Multi-color smooth-edged animated wipe

#### D. Algorithmic Effects
Mathematical screen division algorithms:
- **Blinds 3 Expand**: 3-rectangle algorithmic expansion

## Implementation Details

### Uniform System
Each effect communicates with the shader via OpenGL uniforms:
- `uTime`: Floating-point time value for animation (frameCount * 0.016)
- `uResolution`: Vector2 containing canvas width and height

### Coordinate Systems
- **Screen Space**: p5.js uses pixels (0,0 at top-left)
- **Clip Space**: WebGL shaders use normalized device coordinates (-1 to 1)
- **UV Space**: Texture coordinates (0 to 1)

### Effect Status Tracking
The `index.html` serves as the central status dashboard:
- Gray (unimplemented): Not yet coded
- Green (success): Effect loads without errors
- Red (failure): Effect has unresolved errors after 20 attempts

## Development Workflow

Based on docs/PLAN.md:
1. Read effect description from `ref/video_toaster_methods.md`
2. Create HTML file with p5.js boilerplate
3. Implement GLSL shader based on original hardware description
4. Test via headless browser (up to 20 iterations)
5. Update status in `index.html`

## Original Hardware Reference

The Video Toaster (1990s) used:
- **Amiga graphics**: 256-color palettes (AGA) or 16-color (OCS/ECS)
- **CrUD format**: Crouton User Data files defining effect behavior
- **Video mixing**: AMUX/BMUX with 4-level DIB fader
- **Resolution**: 640x480 interlaced NTSC

The modern implementation abstracts these hardware constraints into pure mathematical operations using GLSL.

## Current Status

- **Total Effects**: 14
- **Successful Implementations**: 14
- **Failed Implementations**: 0
- **Success Rate**: 100%

## Performance Considerations

- Uses `mediump` precision for mobile compatibility
- Single quad rendering (2 triangles) for all effects
- No external textures (procedural generation only)
- Real-time shader computation (no pre-baked frames)

## Future Enhancements

Potential improvements to the architecture:
- Shared shader utilities/common functions
- Interactive parameters via UI controls
- Video input support (Webcam/Canvas)
- Effect chaining/composition
- WASM-based effect simulation (closer to original hardware timing)

---
*Generated: 2026-04-09*
