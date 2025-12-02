import requests
import os
import socket
import re

print("Host:", socket.gethostname())
print("CWD:", os.getcwd())

SYSTEM = """You are an advanced music recommendation system.

Task:
Given a user's listening history, generate the top 10 recommended music items for that user.
When providing recommendations, explain your reasoning step by step, considering factors such as genre, artist similarity, popularity, and user preferences.

Output format:
<thinking>
{your reasoning steps here}
</thinking>

<answer>
[ "{item1}", "{item2}", "{item3}", "{item4}", "{item5}", "{item6}", "{item7}", "{item8}", "{item9}", "{item10}" ]
</answer>

Examples:

Example 1:
The user with id 15 listened Cliff Richard 1970s|Stop This Flight|16 Smash Hits by The Monkees|After The Gold Rush: The Dawn/Pye Anthology 1973-77 by Prelude (2006-09-25)|Remembering The Sixties, 1964|What You Need|The Country Store Collection|An aching and a longing [Vinyl-LP]|Preachers From Outer Space by Daniel Amos (Audio CD)|Eric Clapton: Give Me Strength: The 1974/1975 Studio Recordings 
Based on his or her listened music history, the top 10 recommended item is in the following: Mt. Pleasant|Your Hit Parade - 1946|A New Sunrise|Popemobile|Getting Down - 20 Blues Classics - by Lowell Fulson (Audio CD)|Stress Why You Put Me Through It|THE Great Soap Opera Themes the New Christy Minstrels [ 8 Track Stereo Tape]|MARIA LUISA LANDIN LA HORA AZUL|Living in a Bubble|Sleeping with the Past / Reg Strikes Back

Example 2:
The user with id 51 listened Running Out of Time|Classic Metal|Underground Metal 2|Tourniquet, Vol. 2|Nobody Special|Underground Metal|Rock N Race|End of the Age: The Best of Bride|Keep the Fire Burning / The World of You and I 45 rpm|Voice 
Based on his or her listened music history, the top 10 recommended item is in the following: Blu Blowin|60 EXITOS DE TRIO CALAVERAS|RUDOLF FIRKUSNY- SMETANA- CZECH POLKAS AND DANCES|15 EXITOS|Songs About Sex and Depression|Cumbias Con Arpa|Janus|Heyday|Orquesta Reve & Neno Gonzalez : Mano a Mano|Apples of Gold

Example 3:
The user with id 43 listened The Road to Canso|Aoi Ie De Bokura Kurasu|Sangre Mia|Face aux Elements Dechaines by Etron Fou Leloublan|Holy Smokes|Tricot - Kabuku Ep [Japan CD] XQMZ-1001|still a Sigure virgin?|Live! Skipper's Smokehouse 8/15/03 & 9/7/03|Culture Shock|Zyacalanda 
Based on his or her listened music history, the top 10 recommended item is in the following: The Great British Psychedelic Trip, Vol. 3|The Best of Sam Cooke|I'M MOVIN ON|Johann Strauss, Jr. ~ Readers Digest Favorites From the Classics|The Swingle Singers Compilation Album (Reflections & Live at Ronnie Scotts)|Laura Smith|Billy Lamont Meets Chuck Edwards|Bear Tracks: Special Bear Exports|Ferruccio Busoni - Berceuse Elegiaque op 42, Canto della Ronda degli Spirit op 47, Lustspielouverture op 38, Four Songs, Violin Concerto in D op 35a, Rondo Arlecchinesco op 46|Scherrer/Fritz: Symphonies & Violin Concerto

Prompt reminder:
Please follow the specified output format strictly without any deviations.
"""

def query_ollama_chat(model, prompt_question, max_token = 2048):
    payload = {
        "model": model,
        "stream": False,
        "options": {"temperature": 0,
                    "num_gpu": 1, #change to cpu, I think it can run on your local desk
                    "max_tokens": max_token},
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt_question}
        ]
    }
    r = requests.post("http://localhost:11434/api/chat", json=payload, timeout=None)
    r.raise_for_status()
    data = r.json()
    return (data.get("message") or {}).get("content","").strip()

with open("../Data/input.txt", encoding="utf-8") as f, \
     open("CoT_reasoning_process.txt", "w", encoding="utf-8") as reasoning_file, \
     open("CoT_recommendations.txt", "w", encoding="utf-8") as recommendations_file:
    
    for line in f:
        t = line.strip()
        
        # Extract user ID from the prompt
        user_id_match = re.search(r'The user with id (\d+)', t)
        user_id = user_id_match.group(1) if user_id_match else "unknown"
        
        g = query_ollama_chat('gemma3:4b', t)
        
        # Parse the output to extract thinking and answer sections
        thinking_match = re.search(r'<thinking>(.*?)</thinking>', g, re.DOTALL)
        answer_match = re.search(r'<answer>(.*?)</answer>', g, re.DOTALL)
        
        if thinking_match:
            reasoning_file.write(f"User ID: {user_id}\n{thinking_match.group(1).strip()}\n\n")
        else:
            print("No <thinking> section found.")
        
        if answer_match:
            recommendations_file.write(f"{answer_match.group(1).strip()}\n")
        else:
            print("No <answer> section found.")
            recommendations_file.write("[]\n")
        
