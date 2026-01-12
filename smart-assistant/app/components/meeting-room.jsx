"use client"


import React, { useEffect, useRef, useState } from 'react'
// import { useStreamClients } from '../hooks/use-stream-client'
import { CallControls, SpeakerLayout, StreamCall, useStreamVideoClient } from '@stream-io/video-react-sdk'
import "@stream-io/video-react-sdk/dist/css/styles.css";
import TranscriptPanel from './transcipt';

const MeetingRoom = ({ callId, onLeave, userId }) => {
    const client = useStreamVideoClient()
    const [call, setCall] = useState(null)
    const [error, setError] = useState(null)

    const joinedRef = useRef(false)
    const leavingRef = useRef(false)

    const callType = "default"

    useEffect(() => {
        if (!client || joinedRef.current) return
        joinedRef.current = true

        const init = async () => {
            try {
                const myCall = client.call(callType, callId)
                await myCall.getOrCreate({
                    data: {
                        created_by_id: userId,
                        members: [{ user_id: userId, role: "call_member" }]
                    }
                })
                await myCall.join()
                await myCall.startClosedCaptions({ language: "en" })
                myCall.on("call.session_ended", () => {
                    console.log("Session ended")
                    onLeave?.()
                })
                setCall(myCall)


            } catch (error) {
                setError(error.message)
            }
        }

        init()

        return () => {
            if (call && !leavingRef.current) {
                leavingRef.current = true
                call.stopClosedCaptions().catch(() => { })
                call.leave().catch(() => { })
            }
        }

    }, [client, callId, userId])

    if (error) {
        return (
            <div className='flex items-center justify-center min-h-screen text-white'>
                Error: {error}
            </div>
        )
    }

    if (!call) {
        return (
            <div className='flex items-center justify-center min-h-screen text-white'>
                <div className='animate-spin h-16 w-16 border-t-4 border-blue-500 rounded-full'>
                    <p className='mt-4 text-lg'>Loading meeting...</p>
                </div>
            </div>
        )
    }

    const handleLeave = async () => {
        if (leavingRef.current) {
            onLeave?.()
            return
        }

        leavingRef.current = true
        try {
            if (call) {

                call.stopClosedCaptions().catch(() => { })
                call.leave().catch(() => { })
            }
        } catch (error) {
            console.error("Error Leaving Call:", error)
        } finally {
            onLeave?.(

            )
        }
    }
    return (
        <StreamCall call={call}>
            <div className='min-h-screen bg-linear-to-br from-gray-900 via-gray-800 to-gray-900 text-white container mx-auto px-4 py-6 ovh'>
                <div className='grid grid-cols-1 lg:grid-cols-[1fr_420px] gap-6 h-screen'>
                    <div className='flex flex-col gap-4'>
                        <div className='flex-1 rounded-xl bg-gray-800 border border-gray-700 shadow-2xl overflow-hidden '>
                            <SpeakerLayout />
                        </div>
                        <div className='flex justify-center pb-4 rounded-full bg-gray-800 border border-gray-700 shadow-xl mx-auto px-8 py-4 w-fit'>
                            <CallControls onLeave={handleLeave} />
                        </div>
                    </div>

                    <div className='bg-gray-800 rounded-2xl border border-gray-700 overflow-hidden shadow-2xl px-4'>
                        <TranscriptPanel />
                    </div>
                </div>
            </div>
        </StreamCall >
    )
}

export default MeetingRoom
