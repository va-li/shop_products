// ==UserScript==
// @name         Extract product groups from BILLA Shop
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Clicks through the product groups and pulls out their names and product group IDs
// @author       Valentin Bauer
// @match        https://shop.billa.at/
// @icon         https://www.google.com/s2/favicons?sz=64&domain=billa.at
// @grant        none
// ==/UserScript==
'use strict';

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const productGroups = {}

window.productGroups = productGroups

async function main() {
    await sleep(2000);

    let sortiment = document.getElementsByClassName("header__dropdown")[0]
    sortiment.click()

    let nav = document.getElementsByClassName("assortment-nav__subimg-container")[0]

    const firstNav = nav.getElementsByClassName("assortment-nav--first")[0]

    for (const btnL1 of firstNav.children[1].getElementsByTagName("button")) {

        const nameL1 = btnL1.getElementsByTagName("span")[0].innerText
        const secondLevelGroup = {}

        productGroups[nameL1] = {
            name: nameL1,
            fullPath: [nameL1],
            url: null, // not known yet
            id: null, // not known yet
            subGroups: secondLevelGroup
        }

        btnL1.click()
        await sleep(100)
        const secondNav = nav.getElementsByClassName("assortment-nav--sub")[0]

        for (const link of secondNav.getElementsByTagName("a")) {

            const nameL2 = link.getElementsByTagName("span")[0].innerText
            const urlL2 = link.href
            const idL2 = urlL2.split("/").pop()

            if (nameL2 == "Unsere Empfehlungen") {
                productGroups[nameL1].id = idL2
                productGroups[nameL1].url = urlL2
            } else {
                secondLevelGroup[nameL2] = {
                    name: nameL2,
                    fullPath: [nameL1, nameL2],
                    url: urlL2,
                    id: idL2,
                    subGroups: null
                }
            }
        }


        for (const btnL2 of secondNav.getElementsByTagName("button")) {

            const nameL2 = btnL2.getElementsByTagName("span")[0].innerText
            const thirdLevelGroup = {}

            secondLevelGroup[nameL2] = {
                name: nameL2,
                fullPath: [nameL1, nameL2],
                url: null, // not known yet
                id: null, // not known yet
                subGroups: thirdLevelGroup
            }

            btnL2.click()
            await sleep(100)
            const thirdNav = nav.getElementsByClassName("assortment-nav ng-scope")[0]

            for (const link of thirdNav.getElementsByTagName("a")) {

                const nameL3 = link.getElementsByTagName("span")[0].innerText
                const urlL3 = link.href
                const idL3 = urlL3.split("/").pop()

                if (nameL3 == "Alle Produkte") {
                    secondLevelGroup[nameL2].id = idL3
                    secondLevelGroup[nameL2].url = urlL3
                } else {
                    thirdLevelGroup[nameL3] = {
                        name: nameL3,
                        fullPath: [nameL1, nameL2, nameL3],
                        url: urlL3,
                        id: idL3,
                        subGroups: null
                    }
                }
            }
        }
    }

};

main();
