/** Telegram Group Security Utility */
import React from "https://esm.sh/react@18.2.0";
import { createRoot } from "https://esm.sh/react-dom@18.2.0/client";

// Placeholder for Telegram Bot Token - would normally use environment variable
const TELEGRAM_BOT_TOKEN = "7909901942:AAEgtEcwAyN3oxFYO0Tqqlfb8vUZYSI8wi8";

// User warning tracking
const userWarnings: Record<number, number> = {};

function App() {
  return (
    <div>
      <h1>🛡️ Telegram Group Security</h1>
      <p>Advanced content moderation utility</p>
    </div>
  );
}

function client() {
  createRoot(document.getElementById("root")).render(<App />);
}
if (typeof document !== "undefined") { client(); }

export default async function server(request: Request): Promise<Response> {
  // Basic webhook handler for Telegram Bot
  if (request.method === "POST") {
    try {
      const update = await request.json();
      
      // Basic security checks
      if (update.message) {
        const chatId = update.message.chat.id;
        const userId = update.message.from.id;
        const username = update.message.from.username;
        const text = update.message.text || '';

        // Simple logging and potential moderation logic
        console.log(`Message from ${username}: ${text}`);

        // Comprehensive list of blocked/sensitive content
        const explicitContentKeywords = [
          'porn', 'sex', 'nude', 'naked', 'xxx', 
          'explicit', 'erotic', 'adult', 'nsfw', 
          'hardcore', 'sexual', 'intercourse'
        ];

        const blockedWords = [
          'spam', 'scam', 'hack', 
          ...explicitContentKeywords
        ];

        // Check for blocked content
        const blockedWordFound = blockedWords.find(word => 
          text.toLowerCase().includes(word)
        );

        if (blockedWordFound) {
          // Track user warnings
          userWarnings[userId] = (userWarnings[userId] || 0) + 1;

          let warningMessage = '';
          if (explicitContentKeywords.includes(blockedWordFound)) {
            warningMessage = `🚫 18+ Content Warning! 
⚠️ Inappropriate content detected. 
👤 User @${username} posted message with explicit terms.
🔞 This is a family-friendly group.`;
          } else {
            warningMessage = `⚠️ Warning: Potential inappropriate content detected from @${username}`;
          }

          // Send warning message
          await sendTelegramMessage(chatId, warningMessage);

          // Escalation for repeated offenses
          if ((userWarnings[userId] || 0) >= 3) {
            await sendTelegramMessage(chatId, `🚨 REPEATED OFFENSE: User @${username} has been warned multiple times. 
Consider taking administrative action.`);
          }
        }
      }
    } catch (error) {
      console.error("Telegram webhook processing error:", error);
    }
  }

  return new Response("Telegram Bot Webhook", { 
    status: 200,
    headers: { "Content-Type": "text/plain" }
  });
}

// Utility function to send Telegram messages
async function sendTelegramMessage(chatId: number, text: string) {
  try {
    const response = await fetch(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        chat_id: chatId,
        text: text
      })
    });
    return await response.json();
  } catch (error) {
    console.error("Failed to send Telegram message:", error);
  }
}

const css = `
body {
  font-family: Arial, sans-serif;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f0f0f0;
}
h1 {
  color: #333;
  text-align: center;
}
`;
