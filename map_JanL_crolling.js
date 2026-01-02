async function GetNaverCafeSearch(menuId, headId, pageSize, pageNum, sortBy='TIME'){
    // https://apis.naver.com/cafe-web/cafe-boardlist-api/v1/cafes/17046257/menus/23/articles
    const url = new URL(`https://apis.naver.com/cafe-web/cafe-boardlist-api/v1/cafes/17046257/menus/${menuId}/articles`);
    if (headId)url.searchParams.set('headId', headId);
    if (pageNum)url.searchParams.set('page', pageNum);
    if (pageSize)url.searchParams.set('pageSize', pageSize);
    if (sortBy)url.searchParams.set('sortBy', sortBy);
    url.searchParams.set('viewType', 'L');
    const res = await fetch(url.toString());
    const b = await res.json();
    return b;
}
const 내가만든유즈맵 = {
    캠페인:235,
    디펜스:369,
    대전:370,
    RPG:371,
    블러드:372,
    미니게임:373,
    컴까기:374,
    서바이벌:375,
    컨트롤:376,
    리듬게임:395,
    퍼즐:397,
    밀리기반:399,
    기타:401,
    디플로메시:403,
    키우기:407,
    어드벤처:409,
    공포:411,
    영상:412,
    탈출:413,
    오펜스:414,
    병맛:415,
    추리:421,
    슈팅:423,
    AOS:425,
    레이싱:428,
}
const 타인제작유즈맵 = {
    캠페인:378,
    디펜스:379,
    대전:380,
    RPG:381,
    블러드:382,
    미니게임:383,
    컴까기:384,
    서바이벌:385,
    컨트롤:377,
    리듬게임:396,
    퍼즐:398,
    밀리기반:400,
    기타:402,
    디플로메시:404,
    키우기:408,
    어드벤처:410,
    공포:416,
    영상:417,
    탈출:418,
    오펜스:419,
    병맛:420,
    추리:422,
    슈팅:424,
    AOS:426,
    호환요청:427,
    레이싱:429
}
async function analyze(menuName, menuId, headMap, analyzeYear, analyzeMonth){
    for (let keyVal of Object.entries(headMap)){
        const headName = keyVal[0];
        const headId = keyVal[1];
        const res = await GetNaverCafeSearch(menuId, headId, 50, 1);
        let count = 0;
        const result = [];
        for(const item of res.result.articleList){
            if (item.item.headId !== headId)
                continue;
            const writeDate = new Date(item.item.writeDateTimestamp);
            const writeYear = writeDate.getFullYear();
            const writeMonth = writeDate.getMonth()+1;  
            if (writeYear !== analyzeYear || writeMonth !== analyzeMonth){
                continue;
            }
            result.push(item.item.subject);
            count++;
        }
        console.log(`${menuName} ${headName} ${count}개\n\t${result.join('\n\t')}`);
    }
}
const analyzeYear = 2025;
const analyzeMonth = 12;
analyze('내가만든유즈맵', 23, 내가만든유즈맵, analyzeYear, analyzeMonth).then(() => {
    analyze('타인제작유즈맵', 26, 타인제작유즈맵, analyzeYear, analyzeMonth);
});