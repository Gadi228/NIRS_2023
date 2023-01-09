const upBtn = document.querySelector('.up-button')
const downBtn = document.querySelector('.down-button')

const btns = document.querySelector('.controls')
const container = document.querySelector('.promo')

const mainSlide = document.querySelector('.main-slide')

const slidesCount = mainSlide.querySelectorAll('.main-slide-eeee').length

let activeSlideIndex = 0



let num = 0


btns.addEventListener('click', event => {
    if (event.target.classList.contains('btn_ul')) {
        num = parseInt(event.target.getAttribute('data-num'))
        changeSlide(num)
    }
})


document.addEventListener('keydown', event => {
    if (event.code == 'ArrowDown' || event.code == 'ArrowLeft') {
        changeSlide('down')
    }
    if (event.code == 'ArrowUp' || event.code == 'ArrowRight') {
        changeSlide('up')
    }
  });


function changeSlide(nue) {
    if (nue === 'up')
        if (num === slidesCount - 1)
            num = 0
        else num++
    else if (nue === 'down')
        if (num === 0)
            num = slidesCount - 1
        else num--
    const width = mainSlide.offsetHeight/slidesCount
    mainSlide.style.transform = `translateY(-${num * width}px)`
}

