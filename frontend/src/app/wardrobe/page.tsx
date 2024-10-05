"use client"

import { useEffect, useRef, useState } from "react";
import { io, Socket } from "socket.io-client";

export default function WardrobePage() {
    const videoRef = useRef<HTMLVideoElement>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const hiddenCanvasRef = useRef<HTMLCanvasElement>(null);
    const [socket, setSocket] = useState<Socket>();

    useEffect(() => {
        // Initialize socket connection
        const socket = io('http://localhost:5000'); // Flask server URL
        setSocket(socket);

        // Capture video feed from user's camera
        async function startVideoStream() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                videoRef.current!.srcObject = stream;

                // Send video frames to the backend
                const sendVideoFrames = () => {
                    const canvas = hiddenCanvasRef.current;
                    const context = canvas!.getContext('2d');
                    context!.drawImage(videoRef.current!, 0, 0, canvas!.width, canvas!.height);

                    // Convert frame to base64
                    const frame = canvas!.toDataURL('image/png', 1);
                    if (socket) {
                        socket.emit('process_frame', { frame }); // Emit the frame to the backend
                    }
                    receiveProcessedFrames(frame);
                };

                videoRef.current!.addEventListener('play', () => {
                    setInterval(sendVideoFrames, 50); // Send frames at 10 FPS
                });
            } catch (error) {
                console.error('Error accessing camera:', error);
            }
        }

        startVideoStream();

        // Receive the processed frames from the server
        async function receiveProcessedFrames(processedFrame: string) {
            //socket.on('processed_frame', (processedFrame) => {
            const image = new Image();
            image.src = processedFrame; // Set the processed frame URL
            image.onload = () => {
                const context = canvasRef.current!.getContext('2d');
                context!.drawImage(image, 0, 0, canvasRef.current!.width, canvasRef.current!.height);
            };
        }

        if (socket) {
            socket.on('video_frame', (frame) => {
                receiveProcessedFrames(frame);
            })
        }

        // });
        // }

        return () => {
            if (socket) {
                socket.disconnect();
            }
        };
    }, []);

    return (<div className="flex-1 flex flex-row">
        <div className="basis-1/6 bg-black p-4 space-y-4 flex flex-col">
            <div className="w-full h-100 px-2 py-10 bg-red-500 rounded"></div>
            <div className="w-full h-100 px-2 py-10 bg-gray-500 rounded" ></div>
            <div className="w-full h-100 px-2 py-10 bg-gray-500 rounded"></div>
            <div className="w-full h-100 px-2 py-10 bg-gray-500 rounded"></div>
            <div className="flex-1" />
        </div>
        <div className="basis-5/6 bg-black flex-col flex p-8">
            <div className="bg-gray-400 rounded-xl flex-1 flex flex-col">
                <video ref={videoRef} className="hidden" autoPlay />
                <canvas ref={hiddenCanvasRef} className="hidden" width={1080} height={760} />
                <canvas ref={canvasRef} className="flex-1 w-full rounded-xl" width={1080} height={540} />
            </div>
        </div>
    </div>)
}