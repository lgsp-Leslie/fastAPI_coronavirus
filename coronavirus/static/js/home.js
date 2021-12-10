;
let home_ops = {
    init() {
        this.filterBind();
        this.getData();
    },
    eventBind() {

    },
    filterBind() {
        let that = this;
        $("#filter").click(() => {
            const city = $("#city").val();
            window.location.href = 'http://' + window.location.host + '/coronavirus?city=' + city;
        });
    },
    getData() {
        let that = this;
        $("#sync").click(() => {
            $.ajax({
                url: '/coronavirus/sync_coronavirus_data/jhu',
                dataType: 'json',
                success(res) {
                    alert('Message:' + res.message)
                }
            })
        });
    }
};

$(document).ready(() => {
    home_ops.init();
});
