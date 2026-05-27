export async function sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export async function playAudio(path: string): Promise<void> {
    const audio = new Audio(path);
    audio.play().catch(error => {
        console.error("播放音频时出错:", error);
    });
}