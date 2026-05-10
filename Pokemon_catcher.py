import asyncio
import logging
import os
import sys
import time
import re
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.errors import FloodWaitError, SessionPasswordNeededError

API_ID   = #TERA API ID DAL [DIRECT DAL DE]
API_HASH = "APNA API HASH KEY DAL"
PHONE_NUMBER = "APNA PHONE NUMBER DAL"

DM_TARGET_USERS = ["Telemon_robot"]
DM_HINT_BOT_USERNAME = "Telemon_robot"
DM_CATCH_COMMAND = "/catch {pokemon_name}"
DM_HINT_INTERVAL = 6.3

GROUP_TARGET_GROUPS = ["gc ka username ghusa yaha", "gc ka username dal", "gc ka username chod de yaha"] #aur bhi gc username sal sakta h,but rate limit lagega jldi,so 2 gc name dal na
GROUP_HINT_BOT_USERNAME = "Telemon_robot"
GROUP_CATCH_COMMAND = "/catch {pokemon_name}"
GROUP_HINT_INTERVAL = 6.3

CUSTOM_MESSAGE = "/use 202"
CUSTOM_MESSAGE_INTERVAL = 5 * 60 
CUSTOM_MESSAGE_ENABLED = True 

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] [%(threadName)s] %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

ALL_POKEMON_NAMES = [
    "bulbasaur", "ivysaur", "venusaur", "charmander", "charmeleon", "charizard",
    "squirtle", "wartortle", "blastoise", "caterpie", "metapod", "butterfree",
    "weedle", "kakuna", "beedrill", "pidgey", "pidgeotto", "pidgeot", "rattata",
    "raticate", "spearow", "fearow", "ekans", "arbok", "pikachu", "raichu",
    "sandshrew", "sandslash", "nidoran-f", "nidorina", "nidoqueen", "nidoran-m",
    "nidorino", "nidoking", "clefairy", "clefable", "vulpix", "ninetales",
    "jigglypuff", "wigglytuff", "zubat", "golbat", "oddish", "gloom", "vileplume",
    "paras", "parasect", "venonat", "venomoth", "diglett", "dugtrio", "meowth",
    "persian", "psyduck", "golduck", "mankey", "primeape", "growlithe", "arcanine",
    "poliwag", "poliwhirl", "poliwrath", "abra", "kadabra", "alakazam", "machop",
    "machoke", "machamp", "bellsprout", "weepinbell", "victreebel", "tentacool",
    "tentacruel", "geodude", "graveler", "golem", "ponyta", "rapidash", "slowpoke",
    "slowbro", "magnemite", "magneton", "farfetchd", "doduo", "dodrio", "seel",
    "dewgong", "grimer", "muk", "shellder", "cloyster", "gastly", "haunter",
    "gengar", "onix", "drowzee", "hypno", "krabby", "kingler", "voltorb", "electrode",
    "exeggcute", "exeggutor", "cubone", "marowak", "hitmonlee", "hitmonchan",
    "lickitung", "koffing", "weezing", "rhyhorn", "rhydon", "chansey", "tangela",
    "kangaskhan", "horsea", "seadra", "goldeen", "seaking", "staryu", "starmie",
    "mr-mime", "scyther", "jynx", "electabuzz", "magmar", "pinsir", "tauros",
    "magikarp", "gyarados", "lapras", "ditto", "eevee", "vaporeon", "jolteon",
    "flareon", "porygon", "omanyte", "omastar", "kabuto", "kabutops", "aerodactyl",
    "snorlax", "articuno", "zapdos", "moltres", "dratini", "dragonair", "dragonite",
    "mewtwo", "mew", "chikorita", "bayleef", "meganium", "cyndaquil", "quilava",
    "typhlosion", "totodile", "croconaw", "feraligatr", "sentret", "furret",
    "hoothoot", "noctowl", "ledyba", "ledian", "spinarak", "ariados", "crobat",
    "chinchou", "lanturn", "pichu", "cleffa", "igglybuff", "togepi", "togetic",
    "natu", "xatu", "mareep", "flaaffy", "ampharos", "bellossom", "marill",
    "azumarill", "sudowoodo", "politoed", "hoppip", "skiploom", "jumpluff", "aipom",
    "sunkern", "sunflora", "yanma", "wooper", "quagsire", "espeon", "umbreon",
    "murkrow", "slowking", "misdreavus", "unown", "wobbuffet", "girafarig", "pineco",
    "forretress", "dunsparce", "gligar", "steelix", "snubbull", "granbull", "qwilfish",
    "scizor", "shuckle", "heracross", "sneasel", "teddiursa", "ursaring", "slugma",
    "magcargo", "swinub", "piloswine", "corsola", "remoraid", "octillery", "delibird",
    "mantine", "skarmory", "houndour", "houndoom", "kingdra", "phanpy", "donphan",
    "porygon2", "stantler", "smeargle", "tyrogue", "hitmontop", "smoochum", "elekid",
    "magby", "miltank", "blissey", "raikou", "entei", "suicune", "larvitar", "pupitar",
    "tyranitar", "lugia", "ho-oh", "celebi", "treecko", "grovyle", "sceptile",
    "torchic", "combusken", "blaziken", "mudkip", "marshtomp", "swampert", "poochyena",
    "mightyena", "zigzagoon", "linoone", "wurmple", "silcoon", "beautifly", "cascoon",
    "dustox", "lotad", "lombre", "ludicolo", "seedot", "nuzleaf", "shiftry", "taillow",
    "swellow", "wingull", "pelipper", "ralts", "kirlia", "gardevoir", "surskit",
    "masquerain", "shroomish", "breloom", "slakoth", "vigoroth", "slaking", "nincada",
    "ninjask", "shedinja", "whismur", "loudred", "exploud", "makuhita", "hariyama",
    "azurill", "nosepass", "skitty", "delcatty", "sableye", "mawile", "aron", "lairon",
    "aggron", "meditite", "medicham", "electrike", "manectric", "plusle", "minun",
    "volbeat", "illumise", "roselia", "gulpin", "swalot", "carvanha", "sharpedo",
    "wailmer", "wailord", "numel", "camerupt", "torkoal", "spoink", "grumpig", "spinda",
    "trapinch", "vibrava", "flygon", "cacnea", "cacturne", "swablu", "altaria",
    "zangoose", "seviper", "lunatone", "solrock", "barboach", "whiscash", "corphish",
    "crawdaunt", "baltoy", "claydol", "lileep", "cradily", "anorith", "armaldo",
    "feebas", "milotic", "castform", "kecleon", "shuppet", "banette", "duskull",
    "dusclops", "tropius", "chimecho", "absol", "wynaut", "snorunt", "glalie", "spheal",
    "sealeo", "walrein", "clamperl", "huntail", "gorebyss", "relicanth", "luvdisc",
    "bagon", "shelgon", "salamence", "beldum", "metang", "metagross", "regirock",
    "regice", "registeel", "latias", "latios", "kyogre", "groudon", "rayquaza",
    "jirachi", "deoxys", "turtwig", "grotle", "torterra", "chimchar", "monferno",
    "infernape", "piplup", "prinplup", "empoleon", "starly", "staravia", "staraptor",
    "bidoof", "bibarel", "kricketot", "kricketune", "shinx", "luxio", "luxray",
    "budew", "roserade", "cranidos", "rampardos", "shieldon", "bastiodon", "burmy",
    "wormadam", "mothim", "combee", "vespiquen", "pachirisu", "buizel", "floatzel",
    "cherubi", "cherrim", "shellos", "gastrodon", "ambipom", "drifloon", "drifblim",
    "buneary", "lopunny", "mismagius", "honchkrow", "glameow", "purugly", "chingling",
    "stunky", "skuntank", "bronzor", "bronzong", "bonsly", "mime-jr", "happiny",
    "chatot", "spiritomb", "gible", "gabite", "garchomp", "munchlax", "riolu",
    "lucario", "hippopotas", "hippowdon", "skorupi", "drapion", "croagunk", "toxicroak",
    "carnivine", "finneon", "lumineon", "mantyke", "snover", "abomasnow", "weavile",
    "magnezone", "lickilicky", "rhyperior", "tangrowth", "electivire", "magmortar",
    "togekiss", "yanmega", "leafeon", "glaceon", "gliscor", "mamoswine", "porygon-z",
    "gallade", "probopass", "dusknoir", "froslass", "rotom", "uxie", "mesprit", "azelf",
    "dialga", "palkia", "heatran", "regigigas", "giratina", "cresselia", "phione",
    "manaphy", "darkrai", "shaymin", "arceus", "victini", "snivy", "servine", "serperior",
    "tepig", "pignite", "emboar", "oshawott", "dewott", "samurott", "patrat", "watchog",
    "lillipup", "herdier", "stoutland", "purrloin", "liepard", "pansage", "simisage",
    "pansear", "simisear", "panpour", "simipour", "munna", "musharna", "pidove",
    "tranquill", "unfezant", "blitzle", "zebstrika", "roggenrola", "boldore", "gigalith",
    "woobat", "swoobat", "drilbur", "excadrill", "audino", "timburr", "gurdurr",
    "conkeldurr", "tympole", "palpitoad", "seismitoad", "throh", "sawk", "sewaddle",
    "swadloon", "leavanny", "venipede", "whirlipede", "scolipede", "cottonee",
    "whimsicott", "petilil", "lilligant", "basculin", "sandile", "krokorok", "krookodile",
    "darumaka", "darmanitan", "maractus", "dwebble", "crustle", "scraggy", "scrafty",
    "sigilyph", "yamask", "cofagrigus", "tirtouga", "carracosta", "archen", "archeops",
    "trubbish", "garbodor", "zorua", "zoroark", "minccino", "cinccino", "gothita",
    "gothorita", "gothitelle", "solosis", "duosion", "reuniclus", "ducklett", "swanna",
    "vanillite", "vanillish", "vanilluxe", "deerling", "sawsbuck", "emolga", "karrablast",
    "escavalier", "foongus", "amoonguss", "frillish", "jellicent", "alomomola", "joltik",
    "galvantula", "ferroseed", "ferrothorn", "klink", "klang", "klinklang", "tynamo",
    "eelektrik", "eelektross", "elgyem", "beheeyem", "litwick", "lampent", "chandelure",
    "axew", "fraxure", "haxorus", "cubchoo", "beartic", "cryogonal", "shelmet",
    "accelgor", "stunfisk", "mienfoo", "mienshao", "druddigon", "golett", "golurk",
    "pawniard", "bisharp", "bouffalant", "rufflet", "braviary", "vullaby", "mandibuzz",
    "heatmor", "durant", "deino", "zweilous", "hydreigon", "larvesta", "volcarona",
    "cobalion", "terrakion", "virizion", "tornadus", "thundurus", "reshiram", "zekrom",
    "landorus", "kyurem", "keldeo", "meloetta", "genesect", "chespin", "quilladin",
    "chesnaught", "fennekin", "braixen", "delphox", "froakie", "frogadier", "greninja",
    "bunnelby", "diggersby", "fletchling", "fletchinder", "talonflame", "scatterbug",
    "spewpa", "vivillon", "litleo", "pyroar", "flabebe", "floette", "florges", "skiddo",
    "gogoat", "pancham", "pangoro", "furfrou", "espurr", "meowstic", "honedge",
    "doublade", "aegislash", "spritzee", "aromatisse", "swirlix", "slurpuff", "inkay",
    "malamar", "binacle", "barbaracle", "skrelp", "dragalge", "clauncher", "clawitzer",
    "helioptile", "heliolisk", "tyrunt", "tyrantrum", "amaura", "aurorus", "sylveon",
    "hawlucha", "dedenne", "carbink", "goomy", "sliggoo", "goodra", "klefki", "phantump",
    "trevenant", "pumpkaboo", "gourgeist", "bergmite", "avalugg", "noibat", "noivern",
    "xerneas", "yveltal", "zygarde", "diancie", "hoopa", "volcanion", "rowlet", "dartrix",
    "decidueye", "litten", "torracat", "incineroar", "popplio", "brionne", "primarina",
    "pikipek", "trumbeak", "toucannon", "yungoos", "gumshoos", "grubbin", "charjabug",
    "vikavolt", "crabrawler", "crabominable", "oricorio", "cutiefly", "ribombee",
    "rockruff", "lycanroc", "wishiwashi", "mareanie", "toxapex", "mudbray", "mudsdale",
    "dewpider", "araquanid", "fomantis", "lurantis", "morelull", "shiinotic", "salandit",
    "salazzle", "stufful", "bewear", "bounsweet", "steenee", "tsareena", "comfey",
    "oranguru", "passimian", "wimpod", "golisopod", "sandygast", "palossand", "pyukumuku",
    "type-null", "silvally", "minior", "komala", "turtonator", "togedemaru", "mimikyu",
    "bruxish", "drampa", "dhelmise", "jangmo-o", "hakamo-o", "kommo-o", "tapu-koko",
    "tapu-lele", "tapu-bulu", "tapu-fini", "cosmog", "cosmoem", "solgaleo", "lunala",
    "nihilego", "buzzwole", "pheromosa", "xurkitree", "celesteela", "kartana", "guzzlord",
    "necrozma", "magearna", "marshadow", "poipole", "naganadel", "stakataka", "blacephalon",
    "zeraora", "meltan", "melmetal", "grookey", "thwackey", "rillaboom", "scorbunny",
    "raboot", "cinderace", "sobble", "drizzile", "inteleon", "skwovet", "greedent",
    "rookidee", "corvisquire", "corviknight", "blipbug", "dottler", "orbeetle", "nickit",
    "thievul", "gossifleur", "eldegoss", "wooloo", "dubwool", "chewtle", "drednaw",
    "yamper", "boltund", "rolycoly", "carkol", "coalossal", "applin", "flapple", "appletun",
    "silicobra", "sandaconda", "cramorant", "arrokuda", "barraskewda", "toxel", "toxtricity",
    "sizzlipede", "centiskorch", "clobbopus", "grapploct", "sinistea", "polteageist",
    "hatenna", "hattrem", "hatterene", "impidimp", "morgrem", "grimmsnarl", "obstagoon",
    "perrserker", "cursola", "sirfetchd", "mr-rime", "runerigus", "milcery", "alcremie",
    "falinks", "pincurchin", "snom", "frosmoth", "stonjourner", "eiscue", "indeedee",
    "morpeko", "cufant", "copperajah", "dracozolt", "arctozolt", "dracovish", "arctovish",
    "duraludon", "dreepy", "drakloak", "dragapult", "zacian", "zamazenta", "eternatus",
    "kubfu", "urshifu", "zarude", "regieleki", "regidrago", "glastrier", "spectrier",
    "calyrex", "wyrdeer", "kleavor", "ursaluna", "basculegion", "sneasler",
    "overqwil", "enamorus", "sprigatito", "floragato", "meowscarada", "fuecoco",
    "crocalor", "skeledirge", "quaxly", "quaxwell", "quaquaval", "lechonk", "oinkologne",
    "tarountula", "spidops", "nymble", "lokix", "pawmi", "pawmo", "pawmot", "tandemaus",
    "maushold", "fidough", "dachsbun", "smoliv", "dolliv", "arboliva", "squawkabilly",
    "nacli", "naclstack", "garganacl", "charcadet", "armarouge", "ceruledge", "tadbulb",
    "bellibolt", "wattrel", "kilowattrel", "maschiff", "mabosstiff", "shroodle", "grafaiai",
    "bramblin", "brambleghast", "toedscool", "toedscruel", "klawf", "capsakid", "scovillain",
    "rellor", "rabsca", "flittle", "espathra", "tinkatink", "tinkatuff", "tinkaton",
    "wiglett", "wugtrio", "bombirdier", "finizen", "palafin", "varoom", "revavroom",
    "cyclizar", "orthworm", "glimmet", "glimmora", "greavard", "houndstone", "flamigo",
    "cetoddle", "cetitan", "veluza", "dondozo", "tatsugiri", "annihilape", "clodsire",
    "farigiraf", "dudunsparce", "kingambit", "great-tusk", "scream-tail", "brute-bonnet",
    "flutter-mane", "slither-wing", "sandy-shocks", "iron-treads", "iron-bundle",
    "iron-hands", "iron-jugulis", "iron-moth", "iron-thorns", "frigibax", "arctibax",
    "baxcalibur", "gimmighoul", "gholdengo", "wo-chien", "chien-pao", "ting-lu", "chi-yu",
    "roaring-moon", "iron-valiant", "koraidon", "miraidon", "walking-wake", "iron-leaves",
    "dipplin", "poltchageist", "sinistcha", "okidogi", "munkidori", "fezandipiti",
    "ogerpon", "archaludon", "hydrapple", "gouging-fire", "raging-bolt", "iron-boulder",
    "iron-crown", "terapagos", "pecharunt"
]

POKEMON_SET = set(ALL_POKEMON_NAMES)
POKEMON_SET_LOWER = {name.lower() for name in ALL_POKEMON_NAMES}

class HintParser:
    
    def __init__(self):
        self.underscore_pattern = re.compile(r"Hint:\s*([A-Za-z_]+)", re.IGNORECASE)
        self.direct_name_pattern = re.compile(r"Hint:\s*([A-Za-z][A-Za-z\s\-]+?)(?:\s|$|\.|!|\n)", re.IGNORECASE)
        
        self.clean_pattern = re.compile(r'^[A-Za-z\s\-]+$')

    def parse_hint(self, text):
        if not text:
            return None

        text = text.strip()
        
        
        underscore_match = self.underscore_pattern.search(text)
        if underscore_match:
            pattern = underscore_match.group(1).strip()
            
            if '_' in pattern:
                length = len(pattern)
                return (pattern, length, False)
            
           
            if pattern and pattern.lower() in POKEMON_SET_LOWER:
                return (pattern.lower(), len(pattern), True)
        
        
        hint_match = re.search(r"Hint:\s*([A-Za-z][A-Za-z\s\-]+)", text, re.IGNORECASE)
        if hint_match:
            potential_name = hint_match.group(1).strip()
            
            potential_name = re.sub(r'\s+', '-', potential_name)
            potential_name = potential_name.rstrip('.').rstrip(')').rstrip('(').strip()
            
            potential_name = re.sub(r'[\d\(\)\[\]\{\}]+$', '', potential_name)
            
            if potential_name.lower() in POKEMON_SET_LOWER:
                return (potential_name.lower(), len(potential_name), True)
            
            potential_name_spaces = potential_name.replace('-', ' ')
            if potential_name_spaces.lower() in POKEMON_SET_LOWER:
                return (potential_name_spaces.lower(), len(potential_name_spaces), True)
        
        if "hint:" in text.lower():
            parts = re.split(r"Hint:", text, flags=re.IGNORECASE)
            if len(parts) >= 2:
                after_hint = parts[1].strip()
                name_match = re.match(r'^([A-Za-z][A-Za-z\s\-]+)', after_hint)
                if name_match:
                    potential_name = name_match.group(1).strip()
                    potential_name = potential_name.replace(' ', '-')
                    if potential_name.lower() in POKEMON_SET_LOWER:
                        return (potential_name.lower(), len(potential_name), True)
        
        return None

    def matches_pattern(self, name, pattern):
        if len(name) != len(pattern):
            return False

        for i, char in enumerate(pattern):
            if char == "_":
                continue  
            if char.lower() != name[i].lower():
                return False

        return True  #deeep ki chudi chut

    def find_matches(self, pattern, length, is_direct_name=False):
        if is_direct_name:
            if pattern.lower() in POKEMON_SET_LOWER:
                return [pattern.lower()]
            return []
        
        matches = []
        for name in ALL_POKEMON_NAMES:
            if len(name) == length and self.matches_pattern(name, pattern):
                matches.append(name)
        return matches

class DMPokemonCatcher:
    def __init__(self):
        self.client = None
        self.seen_msgs = set()
        self.hint_parser = HintParser()
        self.hint_task = None
        self.custom_msg_task = None
        self.resolved_users = []
        self.session_name = "pokemon_session_dm"
        self.mode_name = "DM-MODE"
        self.last_custom_msg_time = 0

    async def start(self):
        logger.info(f"[{self.mode_name}] Starting DM Mode...")
        logger.info(f"[{self.mode_name}] Target users: {DM_TARGET_USERS}")

        self.client = TelegramClient(self.session_name, API_ID, API_HASH)
        await self.client.connect()

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(PHONE_NUMBER)
            code = input(f"[{self.mode_name}] Telegram OTP daalein: ")
            try:
                await self.client.sign_in(PHONE_NUMBER, code)
            except SessionPasswordNeededError:
                pwd = input(f"[{self.mode_name}] 2FA Password daalein: ")
                await self.client.sign_in(password=pwd)

        logger.info(f"[{self.mode_name}] Bot connected!")

        for username in DM_TARGET_USERS:
            try:
                clean_username = username.lstrip('@')
                entity = await self.client.get_entity(clean_username)
                self.resolved_users.append(entity)
                logger.info(f"[{self.mode_name}] User resolved: @{clean_username} -> ID: {entity.id}")
            except Exception as e:
                logger.error(f"[{self.mode_name}] User resolve nahi hua '@{username}': {e}")

        if not self.resolved_users:
            logger.error(f"[{self.mode_name}] Koi bhi target user resolve nahi hua!")
            return False

        self._register_handlers()
        self.hint_task = asyncio.create_task(self._send_hints_periodically())
        
        if CUSTOM_MESSAGE_ENABLED:
            self.custom_msg_task = asyncio.create_task(self._send_custom_message_periodically())
        
        logger.info(f"[{self.mode_name}] DM Mode started successfully!")
        return True

    async def _send_hints_periodically(self):
        while True:   #prime ki jai
            try:
                await asyncio.sleep(DM_HINT_INTERVAL)
                for user in self.resolved_users:
                    try:
                        await self.client.send_message(user, "/hint")
                        logger.info(f"[{self.mode_name}] Sent /hint to {user.first_name or user.username}")
                    except FloodWaitError as e:
                        logger.warning(f"[{self.mode_name}] Flood wait {e.seconds}s")
                        await asyncio.sleep(e.seconds)
                        await self.client.send_message(user, "/hint")
                    except Exception as e:
                        logger.error(f"[{self.mode_name}] Failed to send /hint: {e}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[{self.mode_name}] Hint task error: {e}")

    async def _send_custom_message_periodically(self):
        while True:
            try:
                await asyncio.sleep(CUSTOM_MESSAGE_INTERVAL)
                
                for user in self.resolved_users:
                    try:
                        await self.client.send_message(user, CUSTOM_MESSAGE)
                        logger.info(f"[{self.mode_name}] Sent custom message '{CUSTOM_MESSAGE}' to {user.first_name or user.username}")
                    except FloodWaitError as e:
                        logger.warning(f"[{self.mode_name}] Flood wait {e.seconds}s on custom message")
                        await asyncio.sleep(e.seconds)
                        await self.client.send_message(user, CUSTOM_MESSAGE)
                    except Exception as e:
                        logger.error(f"[{self.mode_name}] Failed to send custom message: {e}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[{self.mode_name}] Custom message task error: {e}")

    def _register_handlers(self):
        @self.client.on(events.NewMessage(incoming=True))
        async def on_private_message(event):
            if event.is_private:
                await self._process_message(event)
        
        @self.client.on(events.NewMessage(outgoing=True))
        async def on_outgoing_message(event):
            if event.is_private:
                await self._process_message(event)

    async def _process_message(self, event):
        msg = event.message
        uid = f"dm_{event.chat_id}_{msg.id}"

        if uid in self.seen_msgs:
            return
        self.seen_msgs.add(uid)
        if len(self.seen_msgs) > 500:
            self.seen_msgs = set(list(self.seen_msgs)[-250:])

        if msg.media:
            return

        text = msg.raw_text or ""
        
        is_from_target = False
        for target in self.resolved_users:
            if event.sender_id == target.id:
                is_from_target = True
                break

        if not is_from_target:
            return

        hint_result = self.hint_parser.parse_hint(text)
        if hint_result:
            value, length, is_direct_name = hint_result
            
            if is_direct_name:
                logger.info(f"[{self.mode_name}] ✅ DIRECT POKEMON NAME DETECTED: {value}")
                pokemon = value
                catch_msg = DM_CATCH_COMMAND.format(pokemon_name=pokemon)
                try:
                    await self.client.send_message(event.chat_id, catch_msg)
                    logger.info(f"[{self.mode_name}] 🎯 SENT CATCH (direct): {catch_msg}")
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
                    await self.client.send_message(event.chat_id, catch_msg)
                return
            
            logger.info(f"[{self.mode_name}] 🔍 Pattern detected: {value} ({length} letters)")
            matches = self.hint_parser.find_matches(value, length, is_direct_name)
            logger.info(f"[{self.mode_name}] Found {len(matches)} matches")

            if len(matches) == 1:
                pokemon = matches[0]
                catch_msg = DM_CATCH_COMMAND.format(pokemon_name=pokemon)
                try:
                    await self.client.send_message(event.chat_id, catch_msg)
                    logger.info(f"[{self.mode_name}] 🎯 SENT CATCH: {catch_msg}")
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
                    await self.client.send_message(event.chat_id, catch_msg)
            elif len(matches) > 1:
                logger.info(f"[{self.mode_name}] Multiple matches ({len(matches)}), waiting...")
            else:
                logger.warning(f"[{self.mode_name}] No matches found for pattern: {value}")
        else:
            if "hint" in text.lower():
                logger.debug(f"[{self.mode_name}] Unparsed hint text: {text[:100]}")

    async def run(self):
        await self.client.run_until_disconnected()

    async def stop(self):
        if self.hint_task:
            self.hint_task.cancel()
        if self.custom_msg_task:
            self.custom_msg_task.cancel()
        if self.client:
            await self.client.disconnect()

class GroupPokemonCatcher:
    def __init__(self):
        self.client = None
        self.seen_msgs = set()
        self.hint_parser = HintParser()
        self.hint_task = None
        self.custom_msg_task = None
        self.resolved_groups = []
        self.session_name = "pokemon_session_group"
        self.mode_name = "GROUP-MODE"

    async def start(self):
        logger.info(f"[{self.mode_name}] Starting Group Mode...")
        logger.info(f"[{self.mode_name}] Target groups: {GROUP_TARGET_GROUPS}")

        self.client = TelegramClient(self.session_name, API_ID, API_HASH)
        await self.client.connect()

        if not await self.client.is_user_authorized():
            await self.client.send_code_request(PHONE_NUMBER)
            code = input(f"[{self.mode_name}] Telegram OTP daalein: ")
            try:
                await self.client.sign_in(PHONE_NUMBER, code)
            except SessionPasswordNeededError:
                pwd = input(f"[{self.mode_name}] 2FA Password daalein: ")
                await self.client.sign_in(password=pwd)

        logger.info(f"[{self.mode_name}] Bot connected!")   #join @team7x_chat

        for username in GROUP_TARGET_GROUPS:
            try:
                clean_username = username.lstrip('@')
                entity = await self.client.get_entity(clean_username)
                self.resolved_groups.append(entity)
                logger.info(f"[{self.mode_name}] Group resolved: @{clean_username} -> ID: {entity.id}")
            except Exception as e:
                logger.error(f"[{self.mode_name}] Group resolve nahi hua '@{username}': {e}")

        if not self.resolved_groups:
            logger.error(f"[{self.mode_name}] Koi bhi group resolve nahi hua!")
            return False

        self._register_handlers()
        self.hint_task = asyncio.create_task(self._send_hints_periodically())
        
        if CUSTOM_MESSAGE_ENABLED:
            self.custom_msg_task = asyncio.create_task(self._send_custom_message_periodically())
        
        logger.info(f"[{self.mode_name}] Group Mode started successfully!")
        return True

    async def _send_hints_periodically(self):
        while True:
            try:
                await asyncio.sleep(GROUP_HINT_INTERVAL)
                for group in self.resolved_groups:
                    try:
                        await self.client.send_message(group, "/hint")
                        logger.info(f"[{self.mode_name}] Sent /hint to group {group.id}")
                    except FloodWaitError as e:
                        logger.warning(f"[{self.mode_name}] Flood wait {e.seconds}s")
                        await asyncio.sleep(e.seconds)
                        await self.client.send_message(group, "/hint")
                    except Exception as e:
                        logger.error(f"[{self.mode_name}] Failed to send /hint: {e}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[{self.mode_name}] Hint task error: {e}")

    async def _send_custom_message_periodically(self):
        while True:
            try:
                await asyncio.sleep(CUSTOM_MESSAGE_INTERVAL)
                
                for group in self.resolved_groups:
                    try:
                        await self.client.send_message(group, CUSTOM_MESSAGE)
                        logger.info(f"[{self.mode_name}] Sent custom message '{CUSTOM_MESSAGE}' to group {group.id}")
                    except FloodWaitError as e:
                        logger.warning(f"[{self.mode_name}] Flood wait {e.seconds}s on custom message")
                        await asyncio.sleep(e.seconds)
                        await self.client.send_message(group, CUSTOM_MESSAGE)
                    except Exception as e:
                        logger.error(f"[{self.mode_name}] Failed to send custom message: {e}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[{self.mode_name}] Custom message task error: {e}")

    def _register_handlers(self):
        @self.client.on(events.NewMessage(chats=self.resolved_groups))
        async def on_group_message(event):
            await self._process_message(event)

    async def _process_message(self, event):
        msg = event.message
        uid = f"group_{event.chat_id}_{msg.id}"

        if uid in self.seen_msgs:
            return
        self.seen_msgs.add(uid)
        if len(self.seen_msgs) > 500:
            self.seen_msgs = set(list(self.seen_msgs)[-250:])

        if msg.media:
            return

        text = msg.raw_text or ""
        sender = msg.sender

        is_from_hint_bot = False
        if sender and hasattr(sender, 'username') and sender.username:
            if GROUP_HINT_BOT_USERNAME.lower() in sender.username.lower():
                is_from_hint_bot = True
        elif sender and hasattr(sender, 'bot') and sender.bot:
            is_from_hint_bot = True

        if not is_from_hint_bot:
            return

        hint_result = self.hint_parser.parse_hint(text)
        if hint_result:
            value, length, is_direct_name = hint_result
            
            if is_direct_name:
                logger.info(f"[{self.mode_name}] ✅ DIRECT POKEMON NAME DETECTED: {value}")
                pokemon = value
                catch_msg = GROUP_CATCH_COMMAND.format(pokemon_name=pokemon)
                try:
                    await self.client.send_message(event.chat_id, catch_msg)
                    logger.info(f"[{self.mode_name}] 🎯 SENT CATCH (direct): {catch_msg}")
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
                    await self.client.send_message(event.chat_id, catch_msg)
                return
            
            logger.info(f"[{self.mode_name}] 🔍 Pattern detected: {value} ({length} letters)")
            matches = self.hint_parser.find_matches(value, length, is_direct_name)
            logger.info(f"[{self.mode_name}] Found {len(matches)} matches")

            if len(matches) == 1:
                pokemon = matches[0]
                catch_msg = GROUP_CATCH_COMMAND.format(pokemon_name=pokemon)
                try:
                    await self.client.send_message(event.chat_id, catch_msg)
                    logger.info(f"[{self.mode_name}] 🎯 SENT CATCH: {catch_msg}")
                except FloodWaitError as e:
                    await asyncio.sleep(e.seconds)
                    await self.client.send_message(event.chat_id, catch_msg)
            elif len(matches) > 1:
                logger.info(f"[{self.mode_name}] Multiple matches ({len(matches)}), waiting...")
            else:
                logger.warning(f"[{self.mode_name}] No matches found for pattern: {value}")

    async def run(self):
        await self.client.run_until_disconnected()

    async def stop(self):
        if self.hint_task:
            self.hint_task.cancel()
        if self.custom_msg_task:
            self.custom_msg_task.cancel()
        if self.client:
            await self.client.disconnect()

class MultiModeController:
    def __init__(self):
        self.dm_bot = DMPokemonCatcher()
        self.group_bot = GroupPokemonCatcher()
        self.dm_task = None
        self.group_task = None

    async def start_all(self):
        logger.info("=" * 60)
        logger.info("Starting Multi-Mode Pokemon Catcher Bot")
        logger.info(f"Custom message '{CUSTOM_MESSAGE}' will be sent every {CUSTOM_MESSAGE_INTERVAL // 60} minutes")
        logger.info("=" * 60)
        
        dm_success = await self.dm_bot.start()
        if dm_success:
            self.dm_task = asyncio.create_task(self.dm_bot.run())
            logger.info("✓ DM Mode is running")
        else:
            logger.error("✗ DM Mode failed to start")
        
        group_success = await self.group_bot.start()
        if group_success:
            self.group_task = asyncio.create_task(self.group_bot.run())
            logger.info("✓ Group Mode is running")
        else:
            logger.error("✗ Group Mode failed to start")
        
        tasks = []
        if self.dm_task:
            tasks.append(self.dm_task)
        if self.group_task:
            tasks.append(self.group_task)
        
        if tasks:       #free by @cxqok
            await asyncio.gather(*tasks)
        else:
            logger.error("No modes started successfully!")

    async def stop_all(self):
        logger.info("Stopping all modes...")
        if self.dm_task:
            self.dm_task.cancel()
        if self.group_task:
            self.group_task.cancel()
        
        await self.dm_bot.stop()
        await self.group_bot.stop()
        logger.info("All modes stopped.")

async def cxqok():
    controller = MultiModeController()
    try:
        await controller.start_all()
    except KeyboardInterrupt:
        logger.info("\nKeyboard interrupt received...")
        await controller.stop_all()
        logger.info("Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(cxqok())
    except KeyboardInterrupt:
        logger.info("Bot stopped.")