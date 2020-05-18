import requests
import re
import csv

print("""
##############################################
##########                          ##########
########   Crunchyroll meta fetcher   ########
##########                          ##########
##############################################
""")

link = input('Show link, use the show link not episodes:\n')
req = requests.get(link)


complied_reg = re.compile(r"\.data\('bubble_data', {\"name\":\"(.+)\",\"description\":\"(.+)\",\"")


result = complied_reg.finditer(req.text)

episodes = []

for res in result:
    number = res.group(1).split(sep='-', maxsplit=1).pop(0)
    title = res.group(1).split(sep='-', maxsplit=1).pop()
    episodes.append({
        'episode': number.encode().decode('unicode-escape').strip(),
        'title': title.encode().decode('unicode-escape').strip(),
        'description': res.group(2).encode().decode('unicode-escape').strip()
    })

if (len(episodes) - 4) < 1:
    print('No episodes found, Pleas check the link.')
    input('Press any key to exit...')
    exit()

episodes.reverse()
episodes = episodes[4:]
print('There are {NUMBER} episodes found'.format_map({
    'NUMBER': len(episodes)
}))

csv_target = open('episodes.csv', 'w', encoding='utf-8-sig', newline='')
csv_writer = csv.writer(csv_target)

for ep in episodes:
    csv_writer.writerow([ep['episode']])
    csv_writer.writerow([ep['title']])
    csv_writer.writerow([ep['description']])
    csv_writer.writerow([' '])