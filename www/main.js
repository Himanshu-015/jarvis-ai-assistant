$(document).ready(function () {

    $('.text').textillate({
        loop: true,
        sync: true,
        in: { effect: "bounceIn" },
        out: { effect: "bounceOut" }
    });

    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true
    });

    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: { effect: "fadeInUp" },
        out: { effect: "fadeOutUp" }
    });

    // 🎤 DEFAULT STATE
    $("#MicBtn").show();
    $("#SendBtn").hide();

    // 🎤 MIC BUTTON
    // 🎤 MIC BUTTON (FINAL FIX)
    let micTimeout = null;

    $("#MicBtn").click(function () {
        eel.playAssistantSound();

        $("#Oval").hide();
        $("#SiriWave").show();

        eel.allCommands()();

    // 🔥 CLEAR OLD TIMER
        if (micTimeout) {
            clearTimeout(micTimeout);
        }

    // 🔥 AUTO RESET IF NO RESPONSE
        micTimeout = setTimeout(function () {
            console.log("⏳ No response, resetting UI");

            $("#SiriWave").hide();
            $("#Oval").show();
        }, 7000);   // थोड़ा ज्यादा time (LLM के लिए)
    });

    // ⌨️ TEXT SEND FUNCTION
    function PlayAssistant(message) {

        if (message.trim() !== "") {

            eel.senderText(message);

            $("#chatbox").val("");

            // 🔥 BUTTON RESET
            $("#MicBtn").show();
            $("#SendBtn").hide();

            $("#Oval").hide();
            $("#SiriWave").show();

            eel.executeCommandFromUI(message);
        }
    }

    // 🔥 BUTTON TOGGLE
    function ShowHideButton(message) {

        message = message.trim();

        if (message.length === 0) {
            $("#MicBtn").show();
            $("#SendBtn").hide();
        } else {
            $("#MicBtn").hide();
            $("#SendBtn").show();
        }
    }

    // ✅ INPUT FIX
    $("#chatbox").on("input", function () {
        let message = $(this).val();
        ShowHideButton(message);
    });

    // ✅ CLICK SEND
    $("#SendBtn").click(function () {
        let message = $("#chatbox").val();
        PlayAssistant(message);
    });

    // ✅ ENTER KEY
    $("#chatbox").keydown(function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            let message = $("#chatbox").val();
            PlayAssistant(message);
        }
    });

    // ✅ FOCUS FIX
    $("#chatbox").focus(function () {
        ShowHideButton($(this).val());
    });

});


// FACE AUTH SAFE INIT (ONLY ONCE)
let init_called = false;

window.onload = function () {
    try {
        if (!init_called) {
            init_called = true;

            setTimeout(() => {
                eel.init()();   // ✅ only once
                console.log("Init triggered once");
            }, 500);   // delay important
        }
    } catch (e) {
        console.log("Init error:", e);
    }
};