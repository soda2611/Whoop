const searchInput = document.getElementById('textfield');
const resultDiv = document.getElementById('result');
const headDiv = document.getElementById('title');
const displayDiv = document.getElementById('display-zone');

searchInput.addEventListener('keydown', async function(e) {
    if (e.key === 'Enter') {
        const word = searchInput.value.trim().toLowerCase();
        if (!word) return;

        headDiv.innerText = "";
        resultDiv.innerText = "Đang tìm kiếm...";
        try {
            const response = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
            if (!response.ok) {
            resultDiv.innerText = "Không tìm thấy từ.";
            return;
            }
            const data = await response.json();
            const entry = data[0];
            let html = "";
            headDiv.innerText = capitalizeFirst(`${entry.word}`);
            if (entry.phonetics[1] && entry.phonetics[1].text)
            html += `<span style="font-size: 15px">US: <b>${entry.phonetics[1].text}</b><br></span>`;
            if (entry.phonetics[0] && entry.phonetics[0].text)
            html += `<span style="font-size: 15px">US: <b>${entry.phonetics[0].text}</b><br></span>`;
            html += `<br>`;
            entry.meanings.forEach(meaning => {
            html += `<b>${meaning.partOfSpeech}</b>:<br>`;
            meaning.definitions.forEach((def, idx) => {
                html += `${idx + 1}. ${def.definition}<br>`;
                if (def.example) html += `<span style="color:#0e42d3">• ${def.example}</span><br><br>`;
                else html += `<br>`;
            });
            html += `<br><hr><br>`;
            });
            html = html.slice(0, -12);
            resultDiv.innerHTML = html;
            displayDiv.classList.add("fade_in");
            displayDiv.addEventListener("animationend", () => {
                displayDiv.classList.remove("fade_in");
            });
        } catch (e) {
            resultDiv.innerText = "Lỗi vô định";
        }
    }
});

function capitalizeFirst(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function cleartext(){
    searchInput.value = "";
}