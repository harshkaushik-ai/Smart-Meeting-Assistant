import { StreamVideoClient } from "@stream-io/video-react-sdk";
import { useEffect, useState } from "react";
import { StreamChat } from "stream-chat";

export function useStreamClients({apiKey,user,token}){
    const [videoClient, setVideoClient] = useState(null)
    const [chatClient, setChatClient] = useState(null)

    useEffect(()=>{
        if(!user || !apiKey || !token) return

        let isMounted = true

        const intiClients = async ()=>{
            try {
                const tokenProvider = () => Promise.resolve(token)

                const myVideoClient = new StreamVideoClient({apiKey,user,tokenProvider})
                const myChatClient = StreamChat.getInstance(apiKey)
                await myChatClient.connectUser(user,token)

                if(isMounted){
                    setVideoClient(myVideoClient)
                    setChatClient(myChatClient)
                }

                isMounted = false

            } catch (error) {
                console.log("Client initializtion error:",error)
            }
        }

        intiClients()

        return ()=>{
            isMounted = false
            if(videoClient){
                videoClient.disconnectuser().catch(console.error)
            }
            if(chatClient){
                chatClient.disconnectuser().catch(console.error)
            }
        }
    },[apiKey,user,token])

    return {videoClient,chatClient}
}