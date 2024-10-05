"use client"

import { useEffect, useRef, useState } from "react";

export default function WardrobePage() {
    const videoRef = useRef<HTMLVideoElement>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const hiddenCanvasRef = useRef<HTMLCanvasElement>(null);


    useEffect(() => {
        // Capture video feed from user's camera
        async function startVideoStream() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                videoRef.current!.srcObject = stream;

                // Send video frames to the backend
                const sendVideoFrames = async () => {
                    const canvas = hiddenCanvasRef.current;
                    const context = canvas!.getContext('2d');
                    context!.drawImage(videoRef.current!, 0, 0, canvas!.width, canvas!.height);

                    // Convert frame to base64
                    const frame = canvas!.toDataURL('image/jpeg', 1);

                    const response = await fetch("http://localhost:5000/process_frame", {
                        method: 'POST',
                        body: JSON.stringify({ frame }),
                        headers: {
                            'Content-Type': 'application/json'
                        },
                    });

                    const data = await response.json();
                    receiveProcessedFrames(data.url);
                };

                videoRef.current!.addEventListener('play', () => {
                    setInterval(sendVideoFrames, 3000); // Send frames at 10 FPS
                });
            } catch (error) {
                console.error('Error accessing camera:', error);
            }
        }

        startVideoStream();

        // Receive the processed frames from the server
        async function receiveProcessedFrames(processedFrame: string) {
            const image = new Image();
            image.src = processedFrame; // Set the processed frame URL
            image.onload = () => {
                const context = canvasRef.current!.getContext('2d');
                context!.drawImage(image, 0, 0, canvasRef.current!.width, canvasRef.current!.height);
            };
        }

        // });
        // }
    }, []);

    useEffect(() => {
        setInterval(async () => {
            const response = await fetch('http://localhost:5000/hello');;
            const data = await response.json();
            console.log(data);
        }, 2000)
    }, [])

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