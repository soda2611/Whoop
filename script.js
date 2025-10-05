const searchInput = document.getElementById('textfield');
const resultDiv = document.getElementById('result');

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
                html += `<b>${entry.word}</b><br>`;
                entry.meanings.forEach(meaning => {
                    html += `<i>${meaning.partOfSpeech}</i>:<br>`;
                    meaning.definitions.forEach(def => {
                        html += `- ${def.definition}<br>`;
                        if (def.example) html += `<span style="color:gray">Ví dụ: ${def.example}</span><br>`;
                    });
                });
            });
            resultDiv.innerHTML = html;
        } catch (e) {
            resultDiv.innerText = "Lỗi kết nối hoặc không tìm thấy từ.";
        }
    }
});