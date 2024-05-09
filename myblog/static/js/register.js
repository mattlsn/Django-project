$(function() {
    $("#captcha-btn").click(function(event) {
        let $this = $(this);
        let email = $('input[name="email"]').val();
        // 現在你可以使用 email 變量進行後續操作
        // 例如將 email 發送到服務器以請求驗證碼
        // 注意：這個代碼只是一個示例，可能需要根據你的需求進行更多的處理
        if (!email) {
            alert("請先輸入郵箱");
            return;
        }
        // 取消按紐的點擊事件
        $this.off('click');
        //倒數計時
        let countdown = 60;
        let timer = setInterval(function() {
            if (countdown <= 0) {
                $this.text("獲取驗證碼");
                // 清除定时器
                clearInterval(timer);
                // 重新绑定点击事件
                $this.on('click', function() {
                    // 点击事件处理逻辑
                });
                // 发送 AJAX 请求获取验证码
                $.ajax({
                    url: '/auth/captcha?email=' + email,
                    method: 'GET',
                    success: function(result) {
                        console.log(result);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
            } else {
                $this.text(countdown + " 秒后重新发送");
                countdown--;
            }
        }, 1000);
    });
});
