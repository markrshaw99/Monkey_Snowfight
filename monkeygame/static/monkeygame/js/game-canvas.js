class GameCanvas {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        
        // Virtual game dimensions (original Flash size)
        this.GAME_WIDTH = 600;
        this.GAME_HEIGHT = 400;
        
        // Set actual canvas resolution
        this.canvas.width = this.GAME_WIDTH;
        this.canvas.height = this.GAME_HEIGHT;
        
        // Disable image smoothing for pixel-perfect scaling
        this.ctx.imageSmoothingEnabled = false;
        
        this.setupScaling();
        window.addEventListener('resize', () => this.setupScaling());
    }
    
    setupScaling() {
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        
        // Calculate scale factors
        const scaleX = windowWidth / this.GAME_WIDTH;
        const scaleY = windowHeight / this.GAME_HEIGHT;
        
        // Use the smaller scale to maintain aspect ratio
        let scale = Math.min(scaleX, scaleY);
        
        // Snap to integer scales for crisp pixels (2x, 3x, etc.)
        scale = Math.floor(scale);
        scale = Math.max(1, scale); // Minimum 1x scale
        
        // Apply CSS scaling
        this.canvas.style.width = (this.GAME_WIDTH * scale) + 'px';
        this.canvas.style.height = (this.GAME_HEIGHT * scale) + 'px';
        
        // Center the canvas
        this.canvas.style.position = 'absolute';
        this.canvas.style.left = '50%';
        this.canvas.style.top = '50%';
        this.canvas.style.transform = 'translate(-50%, -50%)';
        this.canvas.style.imageRendering = 'pixelated'; // Crisp scaling
    }
    
    // Convert screen coordinates to game coordinates
    screenToGame(screenX, screenY) {
        const rect = this.canvas.getBoundingClientRect();
        const scaleX = this.GAME_WIDTH / rect.width;
        const scaleY = this.GAME_HEIGHT / rect.height;
        
        return {
            x: (screenX - rect.left) * scaleX,
            y: (screenY - rect.top) * scaleY
        };
    }
}