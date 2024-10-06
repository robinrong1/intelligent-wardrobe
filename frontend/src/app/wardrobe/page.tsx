"use client"

import { Allura, Libre_Bodoni } from 'next/font/google'
import { useSearchParams } from 'next/navigation'
import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'; // Import the Next.js router

const allura = Allura({ weight: '400', subsets: ['latin'] })
const libreBodoni = Libre_Bodoni({ weight: '400', subsets: ['latin'] })

export default function WardrobePage() {
    const router = useRouter(); // Initialize the Next.js router
    const [upper, setUpper] = useState<string[]>([])
    const [lower, setLower] = useState<string[]>([])
    const [upperIndex, setUpperIndex] = useState(0)
    const [lowerIndex, setLowerIndex] = useState(0)
    const [message, setMessage] = useState<string | null>(null) // State to handle success message

    const [sUpper, setSUpper] = useState<string[]>([])
    const [sLower, setSLower] = useState<string[]>([])
    
    const [sUpperIndex, setSUpperIndex] = useState(0)
    const [sLowerIndex, setSLowerIndex] = useState(0)

    const searchParams = useSearchParams();
    const rawSuggest = searchParams.get("suggest")

    useEffect(() => {
        async function init() {
            const data: string[] = await fetch("http://localhost:5000/list-clothing")
                .then(res => res.json())
                .then(data => data.clothes)

            const uppers = []
            const lowers = []
            for (const cloth of data) {
                if (cloth.toLowerCase().endsWith("pant") || cloth.toLowerCase().endsWith("short") || cloth.toLowerCase().endsWith("jean") || cloth.toLowerCase().endsWith("pants")) {
                    lowers.push(cloth)
                } else {
                    uppers.push(cloth)
                }
            }
            console.log(uppers)
            console.log(lowers)
            setUpper(uppers)
            setLower(lowers)

            if (rawSuggest) {
            
            const sUppers = []
            const sLowers = []
            for (const cloth of rawSuggest.split(', ')) {
                if (cloth.toLowerCase().endsWith("pant") || cloth.toLowerCase().endsWith("short") || cloth.toLowerCase().endsWith("jean") || cloth.toLowerCase().endsWith("pants")) {
                    sLowers.push(cloth)
                } else {
                    sUppers.push(cloth)
                }
            }
            console.log(sUppers)
            console.log(sLowers)
            setSUpper(sUppers)
            setSLower(sLowers)
        }
        }

        init()
    }, [])

    // Function to fetch the wardrobe from the server
    const fetchClothes = async () => {
        const data: string[] = await fetch("http://localhost:5000/list-clothing")
            .then(res => res.json())
            .then(data => data.clothes)

        const uppers = []
        const lowers = []
        for (const cloth of data) {
            if (cloth.toLowerCase().endsWith("pant") || cloth.toLowerCase().endsWith("short") || cloth.toLowerCase().endsWith("jean") || cloth.toLowerCase().endsWith("pants")) {
                lowers.push(cloth)
            } else {
                uppers.push(cloth)
            }
        }
        setUpper(uppers)
        setLower(lowers)
    }

    // Upload handler with success message
    const handleUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        if (!event.target.files) return;

        const file = event.target.files[0];
        const formData = new FormData();
        formData.append('file', file);

        // Send the file to the backend
        const response = await fetch("http://localhost:5000/add-clothes", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            // If upload is successful, fetch the updated wardrobe
            fetchClothes();

            // Show success message
            setMessage("Clothing successfully uploaded!");

            // Hide message after 3 seconds
            setTimeout(() => {
                setMessage(null);
            }, 3000);
        }
    }

    useEffect(() => {
        async function update() {
            await fetch("http://localhost:5000/select-clothing", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    top: upper[upperIndex],
                    bottom: lower[lowerIndex]
                })
            })
        }

        if (upper.length && lower.length) {
            update()
        }
    }, [upperIndex, lowerIndex, upper, lower])

    
    useEffect(() => {
        async function update() {
            await fetch("http://localhost:5000/select-clothing", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    top: sUpper[sUpperIndex],
                    bottom: sLower[sLowerIndex]
                })
            })
        }

        update()
    }, [sUpperIndex, sLowerIndex, sUpper, sLower])

    return (
        <div className="flex-1 flex flex-row bg-[#654B70] relative">
            {/* Display message when clothing is uploaded */}
            {message && (
                <div className="absolute top-5 left-1/2 transform -translate-x-1/2 bg-green-500 text-white px-4 py-2 rounded">
                    {message}
                </div>
            )}

            <div className="basis-1/6 p-4 space-y-4 flex flex-col pb-10">
                <div className={"text-white text-bold text-5xl " + libreBodoni.className}>Wardrobe</div>
                <div className="flex flex-col flex-1 bg-[#F1D7EF] rounded-2xl p-5 space-y-14">
                    <div className="flex-1"></div>
                    <div className="w-full h-100 px-4 py-2 bg-white rounded-xl text-[#654B70] font-bold text-center" onClick={() => setUpperIndex(upperIndex + 1 % upper.length)}>Top</div>
                    <div className="w-full h-100 px-4 py-2 bg-white rounded-xl text-[#654B70] font-bold text-center" onClick={() => setLowerIndex(lowerIndex + 1 % lower.length)}>Bottom</div>
                    <div className="w-full h-100 px-4 py-2 bg-white rounded-xl text-[#654B70] font-bold text-center" onClick={() => router.push('/prompt')}>Back to Prompt</div>
                    
                    {
                        rawSuggest && (
                            <>
                            <div className="w-full h-100 px-4 py-2 bg-white rounded-xl text-[#654B70] font-bold text-center" onClick={() => setSUpperIndex(upperIndex + 1 % upper.length)}>Suggested Top</div>
                            <div className="w-full h-100 px-4 py-2 bg-white rounded-xl text-[#654B70] font-bold text-center" onClick={() => setSLowerIndex(lowerIndex + 1 % lower.length)}>Suggested Bottom</div>
                    </>)
                    }
                      {/* Upload button wrapped in label, file input is hidden */}
                      <label className="w-full h-100 px-4 py-2 bg-white rounded-xl text-[#654B70] font-bold text-center cursor-pointer">
                        Upload
                        <input
                            type="file"
                            className="hidden"
                            onChange={handleUpload}
                        />
                    </label>
                    <div className="flex-1"></div>
                </div>
            </div>
            <div className="basis-5/6 flex-col flex p-8">
                <div className="text-8xl basis-1/6 flex flex-row space-x-5">
                    <div className="flex-1"></div>
                    <div className={"text-white text-bold " + libreBodoni.className}>Your</div>
                    <div className={"text-black " + allura.className}>Style</div>
                    <div className="flex-1"></div>
                </div>
                <div className="bg-gray-400 rounded-xl basis-5/6 p-2 border-[#B26AAB] border-8 flex flex-col">
                    <img
                        src="http://localhost:5000/video_feed"
                        alt="Video Stream"
                        className="w-full"
                    />
                </div>
            </div>
        </div>
    )
}
