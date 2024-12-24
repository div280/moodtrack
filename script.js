async function logMood() {
    const moodInput = document.getElementById("moodInput").value.trim();
    const reasonInput = document.getElementById("reasonInput").value.trim();

    if (!moodInput) {
        alert("Mood cannot be empty!");
        return;
    }

    try {
        const response = await fetch("/log_mood", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ mood: moodInput, reason: reasonInput }),
        });

        const data = await response.json();
        if (!response.ok) {
            alert(`Error: ${data.message}`);
            return;
        }

        alert(data.message);
        loadMoodReport(); // Refresh mood report
    } catch (error) {
        alert(`Unexpected error: ${error.message}`);
    }
}

async function loadMoodReport() {
    try {
        const response = await fetch("/get_report", { method: "GET" });
        const data = await response.json();

        if (!response.ok) {
            alert(`Error: ${data.message}`);
            return;
        }

        const reportContainer = document.getElementById("reportContainer");
        reportContainer.innerHTML = "";

        data.entries.forEach((entry) => {
            const entryElement = document.createElement("div");
            entryElement.className = "report-entry";
            entryElement.innerText = `${entry.mood} - ${entry.reason || "No reason"} (${entry.timestamp})`;
            reportContainer.appendChild(entryElement);
        });
    } catch (error) {
        alert(`Unexpected error: ${error.message}`);
    }
}
