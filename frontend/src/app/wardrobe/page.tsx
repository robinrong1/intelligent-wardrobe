"use client"

export default function WardrobePage() {

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
                <img
                    src="http://localhost:5000/video_feed"
                    alt="Video Stream"
                    className="w-full flex-1"
                />
            </div>
        </div>
    </div>)
}