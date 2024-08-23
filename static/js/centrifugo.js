const recentMessage = document.getElementById("recent-answer");


const centrifuge = new Centrifuge(centrifugoUrl, {
    token: centrifugoToken
});

centrifuge.on('connecting', function (ctx) {
    console.log(`connecting: ${ctx.code}, ${ctx.reason}`);
}).on('connected', function (ctx) {
    console.log(`connected over ${ctx.transport}`);
}).on('disconnected', function (ctx) {
    console.log(`disconnected: ${ctx.code}, ${ctx.reason}`);
}).connect();

const sub = centrifuge.newSubscription(channelName);

sub.on('publication', function (ctx) {
    const recentMessageAuthor = recentMessage.querySelector("h4");
    const recentMessageText = recentMessage.querySelector("p");
    document.title = "New answer";

    recentMessage.hidden = false;
    recentMessageAuthor.innerHTML = `Last question (by ${ctx.data.username})`
    recentMessageText.innerHTML = ctx.data.text
    
}).on('subscribing', function (ctx) {
    console.log(`subscribing: ${ctx.code}, ${ctx.reason}`);
}).on('subscribed', function (ctx) {
    console.log('subscribed', ctx);
}).on('unsubscribed', function (ctx) {
    console.log(`unsubscribed: ${ctx.code}, ${ctx.reason}`);
}).subscribe();