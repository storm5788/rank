/**
 * Created by python on 19-8-4.
 */
var vm = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        host:host,


        show_cid_error_message:false,
        cid_error_message:'',
        cid_error:false,


        show_score_error_message:false,
        score_error_message:'',
        score_error:false,

        show_rank:false,

        cid:'',
        score:'',
        ranks:[],
        min:'',
        max:'',

    },
    methods: {

        check_cid:function () {
            if (!this.cid){
                this.cid_error_message='请填写各客户端id',
                this.show_cid_error_message=true
                this.cid_error=true
            }else{

                this.show_cid_error_message=false

                this.cid_error=false

            }
        },
        check_score:function () {

            if(!this.score){
                this.score_error_message='请填写分数',
                this.show_score_error_message=true
                this.score_error=true
            }else if(this.score<1 || this.score>10000000){
                this.score_error_message='分数范围在1-10000000之间',
                this.show_score_error_message=true
                this.score_error=true


            }else{

               this.show_score_error_message=false
                this.score_error=false
            }
        },


        // 表单提交
        on_submit: function () {
            this.check_cid();
            this.check_score();

            event.preventDefault();
            if (this.score_error == false && this.cid_error == false) {

                axios.post('/get_ranks/', {
                    cid: this.cid,
                    score: this.score
                }, {
                    headers: {
                        'X-CSRFToken':getCookie('csrftoken')
                    },
                    responseType: 'json',
                    // withCredentials:true
                })
                    .then(response => {

                         this.score_error_message='操作成功',
                            this.show_score_error_message=true
                        this.cid=''
                        this.score=''

                    })
                    .catch(error => {
                        console.log(error.response)
                    })
            }
        },


        show: function () {
             this.check_cid();

            if (this.cid_error == false){
            var cid = this.cid;
            axios.get('/get_ranks/'+cid+"?max="+this.max+"&min="+this.min, {
                headers: {
                        'X-CSRFToken':getCookie('csrftoken')
                    },
                responseType: 'json'
            })
                .then(response => {
                    this.ranks= response.data.rank_list
                    this.show_rank=true

                })
                .catch(error => {
                    console.log(error.response.data);
                })

                }
        }
    }

});