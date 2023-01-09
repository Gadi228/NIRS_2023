const submenuCats = document.querySelector('.sub-menu-cats')
const submenuCols = document.querySelector('.sub-menu-cols')

const cats = document.querySelector('.naw_for_cat')
const cols = document.querySelector('.naw_for_coll')


cats.addEventListener('mouseover', () => {
        subActive(submenuCats)
})

cats.addEventListener('mouseleave', () => {
        removeActive(submenuCats)
})
cols.addEventListener('mouseover', () => {
        subActive(submenuCols)
})

cols.addEventListener('mouseleave', () => {
        removeActive(submenuCols)
    })



function subActive(element) {
    element.style.display = 'block'
}

function removeActive(element) {
    element.style.display = 'none'

}