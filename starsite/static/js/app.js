async function registerTodo({todoName, todoTime, title = "Todo"}) {
    const reg = await navigator.serviceWorker.getRegistration();
    Notification.requestPermission().then((permission) => {
      if (permission !== "granted") {
        // プッシュ通知許可されない場合エラー
        alert("You have to allow push notifications!");
        return;
      }
  
      // プッシュ通知の登録
      reg.showNotification(title, {
        tag: todoTime,
        body: todoName,
        showTrigger: new TimestampTrigger(todoTime),
        data: {
          url: window.location.href,
        },
      });
    });
  }
self.addEventListener("notificationclick", (event) => {
    event.waitUntil(
      self.clients.matchAll().then((clients) => {
        if (clients.length === 0) {
          // WebAppが存在しない場合、新しいタブへ
          self.clients.openWindow("/");
        } else {
          // 複数タブの場合、1つ目のタブへfocus
          clients[0].focus();
        }
      })
    );
  });
  
function addTodoWithPushNotification() {
  registerTodo("It's time to eat your pills!", new Date().getTime() + 5000, "Doctor's hint");
}