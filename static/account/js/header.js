// Vue.createApp({
//   methods: {
//     onclick(){
//       // ユーザーメニューのオンオフの制御
//       // if (this.Active === false) {
//       //   this.Active = true;
//       // }
//       // else {
//       //   this.Active = false;
//       // }
//       this.Active = !this.Active;
//     }
//   },
//   // アプリ中に使うデータの定義
//   data() {
//     return{
//       Active: false
//     }
//   },
// }).mount('#user-menu');


window.addEventListener('DOMContentLoaded',function() {
  const user_btn = document.querySelector('.user_btn');
  const user_menu = document.querySelector('.user_menu');


  user_btn.addEventListener("mouseover", function () {
    user_menu.classList.add('view');

  })

  user_btn.addEventListener("mouseout", function () {
    window.setTimeout(function() {
      user_menu.classList.remove('view')
    }, 2000);


    
  })

})