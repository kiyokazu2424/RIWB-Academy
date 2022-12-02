// スレッドのオンオフボタン
let thread_btn = document.getElementById('thread-btn');
// スレッドのフォーム
let thread_box = document.getElementById('thread-input');

let changeThreadElement = (el)=> {
  console.log('クリック')
  if(el.style.display=='block'){
    el.style.display='none';
  }else{
    el.style.display='block';
  }

}

//スレッドフォーム関数をボタンクリック時に実行
thread_btn.addEventListener('click', ()=> {
  changeThreadElement(thread_box);
}, false);