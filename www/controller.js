$(document).ready(function () {

    // =============================
    // 🔥 DISPLAY MESSAGE (TOP TEXT)
    // =============================
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        $(".siri-message li:first").text(message);
        $('.siri-message').textillate('start');
    }

    // =============================
    // 🔥 SHOW HOOD
    // =============================
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").show();
        $("#SiriWave").hide();
    }

    // =============================
    // 🔥 USER MESSAGE
    // =============================
    eel.expose(senderText)
    function senderText(message) {
        var chatBox = document.getElementById("chat-canvas-body");

        if (message.trim() !== "") {
            chatBox.innerHTML += `
            <div class="row justify-content-end mb-4">
                <div class="width-size">
                    <div class="sender_message">${message}</div>
                </div>
            </div>`;

            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // =============================
    // 🔥 JARVIS RESPONSE (FIXED)
    // =============================
    let currentJarvisMsg = null;

    eel.expose(receiverText)
    function receiverText(message) {
        var chatBox = document.getElementById("chat-canvas-body");

        if (message.trim() !== "") {

            // 🧠 new message only once
            if (!currentJarvisMsg) {
                let id = "msg_" + Date.now();

                chatBox.innerHTML += `
                <div class="row justify-content-start mb-4">
                    <div class="width-size">
                        <div id="${id}" class="receiver_message"></div>
                    </div>
                </div>`;

                currentJarvisMsg = document.getElementById(id);
            }

            // ✅ overwrite instead of creating new blocks
            currentJarvisMsg.innerHTML = message;

            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // =============================
    // 🔥 RESET MESSAGE (OPTIONAL)
    // =============================
    eel.expose(resetJarvisMsg)
    function resetJarvisMsg() {
        currentJarvisMsg = null;
    }

    // =============================
    // 🔥 LOADER / UI FLOW
    // =============================
    eel.expose(hideLoader)
    function hideLoader() {
        $("#Loader").attr("hidden", true);
        $("#FaceAuth").attr("hidden", false);
    }

    eel.expose(hideFaceAuth)
    function hideFaceAuth() {
        $("#FaceAuth").attr("hidden", true);
        $("#FaceAuthSuccess").attr("hidden", false);
    }

    eel.expose(hideFaceAuthSuccess)
    function hideFaceAuthSuccess() {
        $("#FaceAuthSuccess").attr("hidden", true);
        $("#HelloGreet").attr("hidden", false);
    }

    eel.expose(hideStart)
    function hideStart() {
        $("#Start").attr("hidden", true);

        setTimeout(() => {
            $("#Oval").addClass("animate__animated animate__zoomIn");
            $("#Oval").attr("hidden", false);
        }, 800);
    }

    // =============================
    // 🔥 SEND TEXT TO BACKEND
    // =============================

    document.getElementById("SendBtn").addEventListener("click", sendText);

    document.getElementById("chatbox").addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            sendText();
        }
    });

    function sendText() {
        let input = document.getElementById("chatbox");
        let message = input.value;

        if (message.trim() === "") return;

        // show user message
        senderText(message);

        // reset jarvis message for new response
        currentJarvisMsg = null;

        // send to python
        eel.executeCommandFromUI(message);

        input.value = "";
    }

});