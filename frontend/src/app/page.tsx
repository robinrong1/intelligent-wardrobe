"use client"; // Enable client-side interactivity

import React from 'react';
import { useRouter } from 'next/navigation'; // Import the Next.js router
import background from "@/app/img/homepageimg.png"; // Adjust path if needed

export default function Home() {
    const router = useRouter(); // Initialize the Next.js router

    // Function to handle button clicks and navigate to different pages
    const handleButtonClick = (buttonNumber: number) => {
        if (buttonNumber === 1) {
            router.push('/wardrobe'); // Navigate to the wardrobe page (page.tsx in wardrobe folder)
        } else if (buttonNumber === 2) {
            router.push('/prompt'); // Navigate to the "Prompt Now" page
        }
    };

    return (
        <div style={styles.container}>
            {/* Inline style tag to include Libre Bodoni and Libre Franklin fonts */}
            <style>
                {`
                    @import url('https://fonts.googleapis.com/css2?family=Libre+Bodoni:wght@400;700&display=swap');
                    @import url('https://fonts.googleapis.com/css2?family=Libre+Franklin:wght@400;700&display=swap');
                `}
            </style>
            <div style={styles.panel}>
                <h1 style={styles.heading}>FashioNova</h1>
                <h1 style={styles.text}>
                    Having a tough time finding clothes to wear for the day? 
                    Find your style and dress to impress.
                </h1>
                {/* Buttons Component */}
                <Buttons handleButtonClick={handleButtonClick} />
            </div>
        </div>
    );
}

// Buttons component
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
            <button style={buttonStyles.button1} onClick={() => handleButtonClick(1)}>
                My Wardrobe
            </button>
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
        fontFamily: 'Libre Bodoni, serif', // Apply the Libre Bodoni font
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
