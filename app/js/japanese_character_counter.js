function countCharacters() {
    const text = document.getElementById("japaneseText").value;
    const countNewLines = document.getElementById("countNewLines").checked;
    const countSpaces = document.getElementById("countSpaces").checked;
    const enableComparison = document.getElementById("enablecharComparison").checked; // 比較機能を有効にするチェックボックス
    const targetCountInput = document.getElementById("targetcharacterCount"); // 目標文字数入力フィールド
    const targetCount = parseInt(targetCountInput.value, 10) || 0; // 目標文字数を整数として取得（入力がない場合は0）

    let count = 0;

    // スペースと改行を条件によって加算
    if (countSpaces) {
        count += (text.match(/ /g) || []).length;
    }
    if (countNewLines) {
        count += (text.match(/\n/g) || []).length;
    }

    // それ以外の文字のカウント
    count += text.replace(/\n/g, '').replace(/ /g, '').length;

    // 文字数を表示
    document.getElementById("characterCount").textContent = "文字数: " + count;

    // 目標文字数との比較
    if (enableComparison && targetCount > 0) {
        const insufficientLetters = targetCount - count;
        const insufficiencyMessage = insufficientLetters > 0 ? "目標まであと" + insufficientLetters + "文字です。" : "目標文字数を達成しました。";
        document.getElementById("characterComparison").textContent = insufficiencyMessage;

        // 推奨文字数（目標の85%）との比較
        const recommendedCount = Math.ceil(targetCount * 0.85);
        const recommendedInsufficient = recommendedCount - count;
        const recommendedMessage = recommendedInsufficient > 0 ? "推奨文字数まであと" + recommendedInsufficient + "文字です。" : "推奨文字数を達成しました。";
        document.getElementById("recommendedComparison").textContent = recommendedMessage;
    } else {
        document.getElementById("characterComparison").textContent = ""; // 比較を行わない場合は出力をクリア
        document.getElementById("recommendedComparison").textContent = "";
    }
}
