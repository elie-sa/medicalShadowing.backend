const APP_ID = '531a62c67b5849cb9c94b39ab19198b7';
const TOKEN = sessionStorage.getItem('token');
const CHANNEL = sessionStorage.getItem('room');
let UID = sessionStorage.getItem('UID');
let NAME = sessionStorage.getItem('name');

const client = AgoraRTC.createClient({ mode: 'rtc', codec: 'vp8' });

let localTracks = [];
let remoteUsers = {};

let joinAndDisplayLocalStream = async () => {
    document.getElementById('room-name').innerText = CHANNEL;

    client.on('user-published', handleUserJoined);
    client.on('user-left', handleUserLeft);

    try {
        UID = await client.join(APP_ID, CHANNEL, TOKEN, UID);
    } catch (error) {
        console.error(error);
        window.open('/', '_self');
    }

    // Create only the microphone audio track
    localTracks[0] = await AgoraRTC.createMicrophoneAudioTrack();

    let member = await createMember();

    let player = `<div class="audio-container" id="user-container-${UID}">
                     <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                  </div>`;
    document.getElementById('audio-streams').insertAdjacentHTML('beforeend', player);

    await client.publish([localTracks[0]]);
};

let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user;

    await client.subscribe(user, mediaType);

    if (mediaType === 'audio') {
        user.audioTrack.play();

        let player = document.getElementById(`user-container-${user.uid}`);
        if (player != null) {
            player.remove(); // Remove existing container if any
        }

        let member = await getMember(user);

        player = `<div class="audio-container" id="user-container-${user.uid}">
                    <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                 </div>`;
        document.getElementById('audio-streams').insertAdjacentHTML('beforeend', player);
    }
};

let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid];
    document.getElementById(`user-container-${user.uid}`).remove();
};

let leaveAndRemoveLocalStream = async () => {
    for (let i = 0; localTracks.length > i; i++) {
        localTracks[i].stop();
        localTracks[i].close();
    }

    await client.leave();
    deleteMember();
    window.open('/', '_self');
};

let toggleMic = async (e) => {
    if (localTracks[0].muted) {
        await localTracks[0].setMuted(false);
        e.target.style.backgroundColor = '#fff';
    } else {
        await localTracks[0].setMuted(true);
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)';
    }
};

let createMember = async () => {
    let response = await fetch('/create_member/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: NAME, room_name: CHANNEL, UID: UID }),
    });
    let member = await response.json();
    return member;
};

let getMember = async (user) => {
    let response = await fetch(`/get_member/?UID=${user.uid}&room_name=${CHANNEL}`);
    let member = await response.json();
    return member;
};

let deleteMember = async () => {
    await fetch('/delete_member/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: NAME, room_name: CHANNEL, UID: UID }),
    });
};

window.add
