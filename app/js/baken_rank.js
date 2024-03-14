function calculateRank() {
    const hitRate = document.getElementById('hitRate').value;
    const returnRate = document.getElementById('returnRate').value;
    const returnRankElement = document.getElementById('returnRank');
    const hitRankElement = document.getElementById('hitRank');
    const resultRankElement = document.getElementById('resultRank');

    const hitRateDeviation = document.getElementById('hitRateDeviation');
    const returnRateDeviation = document.getElementById('returnRateDeviation');

    // 平均値と標準偏差
    const averageReturnRate = 75;
    const returnRateStdDev = 13;
    const averageHitRate = 15;
    const hitRateStdDev = 3;

    // 標準偏差の差を計算
    const returnRateDiff = (returnRate - averageReturnRate) / returnRateStdDev;
    const hitRateDiff = (hitRate - averageHitRate) / hitRateStdDev;

    // それぞれのランク付け
    let returnRateRank = '';
    let hitRateRank = '';
    let resultRank = '';

    returnRateRank = rankJudge(returnRateDiff);
    hitRateRank = rankJudge(hitRateDiff);
    resultRank = resultrankJudge(returnRateDiff + hitRateDiff) / 2;

    // ランクによって背景色と文字色を変更
    returnRankElement.style.backgroundColor = rankColor(returnRateRank);
    returnRankElement.style.color = 'white';
    returnRankElement.style.fontSize = '2.5rem';
    hitRankElement.style.backgroundColor = rankColor(hitRateRank);
    hitRankElement.style.color = 'white';
    hitRankElement.style.fontSize = '2.5rem';
    resultRankElement.style.backgroundColor = rankColor(resultRank);
    resultRankElement.style.color = 'white';
    resultRankElement.style.fontSize = '2.5rem';

    // 結果を表示
    resultRankElement.innerHTML = `${resultRank}`;
    returnRankElement.innerHTML = `${returnRateRank}`;
    hitRankElement.innerHTML = `${hitRateRank}`;

    // test項目
    hitRateDeviation.innerHTML = `${Math.round(((hitRateDiff) * 10 + 50) * 100) / 100}`;
    returnRateDeviation.innerHTML = `${Math.round(((returnRateDiff) * 10 + 50) * 100) / 100}`;

    // ランク付けと文字の背景色(文字は白抜き)
    // μ+3σ<=P : S, 金色
    // μ+2σ<=P<μ+3σ : A, オレンジ
    // μ+σ<=P<μ+2σ : B, 赤
    // μ<=P<μ+σ : C, 黄緑
    // μ-σ<=P<μ : D, 水色
    // μ-2σ<=P<μ-σ : E, 紫
    // μ-3σ<=P<μ-2σ : F, 青　
    // P<μ-3σ : G, 灰色
    function rankJudge(diff) {
        switch (true) {
            case diff >= 3:
                return 'S';
            case diff >= 2:
                return 'A';
            case diff >= 1:
                return 'B';
            case diff >= 0:
                return 'C';
            case diff >= -1:
                return 'D';
            case diff >= -2:
                return 'E';
            case diff >= -3:
                return 'F';
            case diff < -3:
                return 'G';
            default:
                return 'Error';
        }
    }

    function resultrankJudge(diff) {
        switch (true) {
            case diff >= 5:
                return 'SS';
            case diff >= 4:
                return 'S+';
            case diff >= 3:
                return 'S';
            case diff >= 2:
                return 'A';
            case diff >= 1:
                return 'B';
            case diff >= 0:
                return 'C';
            case diff >= -1:
                return 'D';
            case diff >= -2:
                return 'E';
            case diff >= -3:
                return 'F';
            default:
                return 'G';
        }
    }

    function rankColor(rank) {
        switch (rank) {
            case 'SS':
            case 'S+':
            case 'S':
                return '#FFCC33';
            case 'A':
                return '#FF6666';
            case 'B':
                return '#FF0000';
            case 'C':
                return '#99CC00';
            case 'D':
                return '#00FFFF';
            case 'E':
                return '#800080';
            case 'F':
                return '#0000FF';
            case 'G':
                return '#808080';
        }
    }
}
