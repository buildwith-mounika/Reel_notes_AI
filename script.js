async function summarizeVideo() {

    const url = document.getElementById("videoUrl").value;
    const language = document.getElementById("language").value; // 👈 Ikkada undali

    if (url === "") {
        alert("Please enter a YouTube URL");
        return;
    }

    document.getElementById("summaryText").innerText =
        "⏳ Generating summary... Please wait.";

    try {

        const response = await fetch("/summarize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url: url,
                language: language
            })
        });

        const data = await response.json();

        document.getElementById("summaryText").innerText = data.summary;

    } catch (error) {

        document.getElementById("summaryText").innerText =
            "Something went wrong!";

        console.log(error);
    }

}
function toggleTheme() {

    document.body.classList.toggle("dark");

    const btn = document.getElementById("themeBtn");

    if (document.body.classList.contains("dark")) {
        btn.innerHTML = '<i class="fa-solid fa-sun"></i>';
    } else {
        btn.innerHTML = '<i class="fa-solid fa-moon"></i>';
    }

}