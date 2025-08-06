class AssetLoader {
    constructor() {
        this.images = new Map();
        this.loadPromises = [];
    }
    
    loadImage(name, path) {
        const img = new Image();
        const promise = new Promise((resolve, reject) => {
            img.onload = () => {
                this.images.set(name, img);
                resolve(img);
            };
            img.onerror = reject;
        });
        
        img.src = path;
        this.loadPromises.push(promise);
        return promise;
    }
    
    async loadAll() {
        await Promise.all(this.loadPromises);
    }
    
    get(name) {
        return this.images.get(name);
    }
    
    // Draw image at game coordinates (always use original 600x400 coordinates)
    drawImage(ctx, imageName, x, y, width = null, height = null) {
        const img = this.get(imageName);
        if (!img) return;
        
        if (width && height) {
            ctx.drawImage(img, x, y, width, height);
        } else {
            ctx.drawImage(img, x, y);
        }
    }
}