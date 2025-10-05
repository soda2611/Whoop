const searchInput = document.getElementById('textfield');
const resultDiv = document.getElementById('result');
const headDiv = document.getElementById('title')

searchInput.addEventListener('keydown', async function(e) {
    if (e.key === 'Enter') {
        const word = searchInput.value.trim().toLowerCase();
        if (!word) return;

        resultDiv.innerText = "Đang tìm kiếm...";

        try {
            const response = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`);
            if (!response.ok) {
                resultDiv.innerText = "Không tìm thấy từ.";
                return;
            }
            const data = await response.json();
            let html = "";
            data.forEach(entry => {
                headDiv.innerText = capitalizeFirst(`${entry.word}`)
                entry.meanings.forEach(meaning => {
                    html += `<b>${meaning.partOfSpeech}</b>:<br>`;
                    meaning.definitions.forEach(def => {
                        html += `- ${def.definition}<br>`;
                        if (def.example) html += `<span style="color:#0e42d3">• ${def.example}</span><br><br>`;
                    });
                    html += `<br><hr><br>`
                });
            });
            html = html.slice(0, -12);
            resultDiv.innerHTML = html;
        } catch (e) {
            resultDiv.innerText = "Lỗi kết nối hoặc không tìm thấy từ.";
        }
    }
});

function capitalizeFirst(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}