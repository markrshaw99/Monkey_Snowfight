const canvas = document.getElementById('game_canvas');
const ctx = canvas.getContext('2d');
// Always draw using the internal size (600x400)
ctx.fillStyle = 'skyblue';
ctx.fillRect(0, 0, canvas.width, canvas.height);