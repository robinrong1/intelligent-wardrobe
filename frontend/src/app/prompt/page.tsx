"use client"; // Enable client-side interactivity
import background from "@/app/img/homepageimg.png";
import {Input} from "@nextui-org/input";
import { useRouter } from 'next/navigation';
import React, { useState } from 'react';

import {  Libre_Bodoni } from 'next/font/google'

const libreBodoni = Libre_Bodoni({ weight: '400', subsets: ['latin'] })

export default function PromptPage() {
    const [text, setText] = useState('')
    const router = useRouter(); // Initialize the Next.js router
   
    const submitHandler = async () => {
        const response = await fetch("http://localhost:5000/prompt", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text} )
        })

        const body = await response.json();

        const clothes = body.clothes;
        router.push('/wardrobe?suggest=' + clothes.join(', '));
    }

    return (<div style={styles.container}>
            {/* Inline style tag to include Libre Bodoni and Libre Franklin fonts */}
            <div style={styles.panel} className={libreBodoni.className}>
            <h1 style={styles.heading} className={libreBodoni.className}>
                    Find your
                </h1>
                <h1 style={styles.heading} className={libreBodoni.className}>New style</h1>
                <input
          type="text"
          placeholder="What's the occasion?"
          className="py-4 px-6 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-purple-500 text-gray-700 bg-white w-80"         
       />
                
                <Buttons handleButtonClick={submitHandler}/>
            </div>
        </div>
    );
}
interface ButtonsProps {
    handleButtonClick: (buttonNumber: number) => void;
}

const Buttons: React.FC<ButtonsProps> = ({ handleButtonClick }) => {
    const buttonStyles = {
        buttonContainer: {
            display: 'flex',
            justifyContent: 'center', // Center the buttons
            gap: '30px', // Add space between buttons
        },
        button1: {
            padding: '10px 20px',
            cursor: 'pointer',
            backgroundColor: '#31124A', // Button background color
            border: 'none', // Remove border
            borderRadius: '5px', // Rounded corners for buttons
            fontSize: '18px',
            fontWeight: 'bold',
            color: 'white',
            fontFamily: 'Helvetica, sans-serif',
        },
        button2: {
            padding: '10px 20px',
            cursor: 'pointer',
            backgroundColor: 'white', // Button background color
            border: 'none', // Remove border
            borderRadius: '5px', // Rounded corners for buttons
            fontSize: '18px',
            fontWeight: 'bold',
            color: '#4E246F',
            fontFamily: 'Helvetica, sans-serif',
        },
    };

    return (
        <div style={buttonStyles.buttonContainer}>
            
            <button style={buttonStyles.button2} onClick={() => handleButtonClick(2)}>
                Prompt Now
            </button>
        </div>
    );
};

// Styles
const styles = {
    
     
    container: {
        backgroundImage: `url(${background.src})`, // Set the path to your image
        backgroundSize: '30%', // Zoom in by increasing the background size
        backgroundPosition: 'center', // Keep the image centered
        height: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        margin: 0,
    },
    panel: {
        backgroundColor: 'rgba(0,0,0,0.8)', // Semi-transparent black
        borderRadius: '1px',
        padding: '50px',
        textAlign: 'center',
        width: '2000px', // Set a fixed width for the panel
        height: 'auto', // Set to auto to adjust height based on content
    },
    heading: {
        color: 'white',
        textAlign: 'center',
        margin: '0 0 20px 0', // Add margin below heading
        fontSize: '100px', // Set font size for heading
    },
    text: {
        fontFamily: 'Times New Roman, serif', // Apply the Times New Roman font
        color: 'white',
        textAlign: 'center',
        margin: '0 0 20px 0', // Add margin below heading
        fontSize: '20px', // Set font size for text
    },
};