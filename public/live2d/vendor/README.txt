Optional local runtime:
- Place `live2dcubismcore.min.js` in this folder.

Expected path:
- `/live2d/vendor/live2dcubismcore.min.js`

Why:
- The mascot component prefers a local Cubism Core runtime.
- If this file is missing, it falls back to Live2D's official direct URL.
- Local is more stable for long-term deployments.
