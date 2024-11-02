const path = require('path')
const fs = require('fs');
const { insert, connect } = require('./insert');
const {uploadFields} = require('./update')

const basePath = path.join(__dirname, '/files/')
let currentFoodPage = -1;
let foodAry = []


const readFile = (path) => {
    // console.log('path:',path)
    if (!fs.existsSync(path)) {
        throw Error('文件不存在：', path)
    }
    return JSON.parse(fs.readFileSync(path, 'utf-8'))
}



const start = () => {
    connect((db) => {
        const insertRow = () => {
            if (!foodAry.length) {
                currentFoodPage++;
                const p1 = path.join(basePath, `/v2/${currentFoodPage}.json`)
                foodAry = readFile(p1)
                console.log('foodAry:',foodAry.length)
            }
            // if (!oldFoodAry.length) {
            //     currentOldFoodPage++;
            //     const p2 = path.join(basePath, `/v1/${currentOldFoodPage}.json`)
            //     oldFoodAry = readFile(p2)
            //     console.log('oldFoodAry:',oldFoodAry.length)
            // }
            const food = foodAry.shift()
            // const oldFood = oldFoodAry.shift();
            // if (food.id !== oldFood.id) {
            //     throw Error(`两个id不一致：oldId:${oldFoodAry.id}, foodId:${food.id}`)
            // }
            insert(db, food, () => {
                insertRow()
            })
        }
        insertRow()
           


    })

}

const startUpdate = ()=>{
    connect((db) => {
        const updateRow = () => {
            // console.log('进入UpdateRow', foodAry.length)
            if (!foodAry.length) {
                currentFoodPage++;
                const p1 = path.join(basePath, `/v1/${currentFoodPage}.json`)
                foodAry = readFile(p1)
            }

            const food = foodAry.shift()
            // console.log('food:',food)
            uploadFields(db, food,[
                'brand',
                'weight',
                'is_liquid',
                'appraise'
            ],['brand',
            'weight',
            'liquid',
            'appraise'], () => {
                // throw Error('更亲成功，强行停止')
                updateRow()
            })
        }
        updateRow()
           


    })
}
startUpdate()
// start()