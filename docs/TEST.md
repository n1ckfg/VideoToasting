# VideoToasting Shader Test Report

**Date:** 2026-04-10  
**Test Method:** Static code analysis (syntax and logical review)  
**Files Reviewed:** 14 effect HTML files

## Summary

| Status | Count | Files |
|--------|-------|-------|
| ✅ Pass | 8 | blinds, push-pull, split, squeeze-zoom, swap, transporter, tumble, index |
| ⚠️ Warning | 6 | neon-bands, blinds-3-expand, trails, trajectory, camera-iris, giraffe |
| ❌ Fail | 0 | - |

## Detailed Findings

### ⚠️ Files with GLSL Warnings

#### 1. neon-bands.html
**Issue:** `smoothstep()` called with `edge0 > edge1` (undefined behavior)  
**Line:** 46  
**Code:**
```glsl
float bandOpacity = smoothstep(bandHeight * 0.4, 0.0, abs(uv.y - bandCenter));
```
**Problem:** `bandHeight * 0.4` (positive) > `0.0`, but GLSL requires `edge0 < edge1`  
**Fix:** Swap the first two arguments: `smoothstep(0.0, bandHeight * 0.4, ...)` or use `1.0 - smoothstep(...)` logic

---

#### 2. blinds-3-expand.html
**Issue:** `smoothstep()` called with `edge0 > edge1` (undefined behavior)  
**Line:** 56  
**Code:**
```glsl
float edgeFade = smoothstep(halfWidth, halfWidth * 0.7, distFromCenter);
```
**Problem:** `halfWidth` > `halfWidth * 0.7`  
**Fix:** `smoothstep(halfWidth * 0.7, halfWidth, distFromCenter)`

---

#### 3. trails.html
**Issue:** `smoothstep()` called with `edge0 > edge1` (undefined behavior)  
**Line:** 40  
**Code:**
```glsl
float obj = smoothstep(0.1, 0.0, dist);
```
**Problem:** `0.1` > `0.0`  
**Fix:** `smoothstep(0.0, 0.1, dist)` or `smoothstep(dist, 0.1, 0.0)`

---

#### 4. trajectory.html
**Issue:** `smoothstep()` called with `edge0 > edge1` (undefined behavior)  
**Line:** 48  
**Code:**
```glsl
float obj = smoothstep(0.2, 0.0, dist);
```
**Problem:** `0.2` > `0.0`  
**Fix:** `smoothstep(0.0, 0.2, dist)`

---

#### 5. camera-iris.html
**Issue:** `smoothstep()` called with `edge0 > edge1` (undefined behavior)  
**Line:** 55  
**Code:**
```glsl
float bladeEffect = smoothstep(bladeWidth, bladeWidth * 0.5, bladeAngle);
```
**Problem:** `bladeWidth` > `bladeWidth * 0.5`  
**Fix:** `smoothstep(bladeWidth * 0.5, bladeWidth, bladeAngle)`

---

#### 6. giraffe.html
**Issue:** `smoothstep()` called with `edge0 > edge1` (undefined behavior)  
**Line:** 54  
**Code:**
```glsl
float smoothEdge = smoothstep(edgeWidth, -edgeWidth, shape);
```
**Problem:** `edgeWidth` (positive) > `-edgeWidth` (negative)  
**Fix:** `smoothstep(-edgeWidth, edgeWidth, shape)`

---

### ✅ Files Passing Static Analysis

| File | Status | Notes |
|------|--------|-------|
| blinds.html | ✅ Pass | Correct syntax, proper GLSL usage |
| push-pull.html | ✅ Pass | Correct syntax, proper GLSL usage |
| split.html | ✅ Pass | Correct syntax, proper GLSL usage |
| squeeze-zoom.html | ✅ Pass | Correct syntax, proper GLSL usage |
| swap.html | ✅ Pass | Correct syntax, proper GLSL usage |
| transporter.html | ✅ Pass | Correct syntax, proper GLSL usage |
| tumble.html | ✅ Pass | Correct syntax, proper GLSL usage |
| index.html | ✅ Pass | HTML structure valid |

## GLSL Specification Reference

Per the GLSL specification, `smoothstep(edge0, edge1, x)` requires `edge0 < edge1`. When `edge0 >= edge1`, the behavior is **undefined** and may result in:
- Compilation errors on strict GPU drivers
- Inconsistent rendering across different hardware
- Unexpected visual artifacts

## Recommendations

1. **Fix smoothstep calls** in the 6 flagged files to ensure `edge0 < edge1`
2. **Runtime testing** required to verify visual correctness of each effect
3. **Cross-browser testing** recommended (Chrome, Firefox, Safari) to ensure WebGL compatibility
4. **Mobile device testing** recommended since `mediump` precision is used

## Test Methodology Notes

This report is based on **static code analysis only**. Actual browser rendering tests were not performed. The warnings above represent potential runtime errors that may cause compilation failures or undefined behavior on certain GPU drivers.

To fully validate these effects, a headless browser (e.g., Puppeteer, Selenium) or manual browser testing is required.
