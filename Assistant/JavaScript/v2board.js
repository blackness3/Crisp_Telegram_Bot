function formatDate(date) {
    year = date.getFullYear();
    month = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1);
    day = date.getDate();
    return year + '-' + month + '-' + day
}

function btogb(n) {
    return (n / 1024 / 1024 / 1024).toFixed(2)
}

async function fetchUserDataFromUrl(url) {
    const myHeaders = new Headers();
    myHeaders.append("Authorization", localStorage.getItem("token"));

    const requestOptions = {
        method: 'GET',
        headers: myHeaders,
        redirect: 'follow'
    };
    const response = await fetch(url, requestOptions);
    const result = await response.json();
    return result;
};

async function crispPush() {

    fetchUserDataFromUrl('/api/v1/user/getSubscribe')
        .then((result) => {
            window.$crisp.push(
                [
                    "set", "session:data", [
                        [
                            ["Plan", (null === (o = result.data.plan) || void 0 === o ? void 0 : o.name) || "-"],
                            ["ExpireTime", formatDate(date = new Date(result.data.expired_at * 1000))],
                            ["UsedTraffic", btogb(result.data.u + result.data.d)],
                            ["AllTraffic", btogb(result.data.transfer_enable)],
                        ]
                    ]
                ]
            );
        }
        )
    fetchUserDataFromUrl('/api/v1/user/info')
        .then((result) => {
            window.$crisp.push(["set", "user:email", result.data.email])
            window.$crisp.push(
                [
                    "set", "session:data", [
                        [
                            ["Balance", result.data.balance / 100]
                        ]
                    ]
                ]
            )
        }
        )
};

(function () {

    function wait(time) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                resolve(time)
            }, time)
        })
    }

    (async () => {
        for (var i = 0; i < 5; i++) {
            if (document.querySelector('.cc-nsge') != null) {
                document.querySelector('.cc-nsge').addEventListener('click', function handleClick(event) {
                    console.debug("try to add eventlistener " + i);
                    crispPush();
                });
                break
            }
            await wait(1000);
        }
    })();

})();
