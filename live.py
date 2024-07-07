# live.py
import http.client
import json
import time
import logging

# Configurar logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_live_events():
    conn = http.client.HTTPSConnection("prod-global-bff-events.bet6.com.br")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json"
    }

    try:
        logging.info("Enviando requisição para a API")
        conn.request("GET", "/api/sports/1/markets/1/live-events", headers=headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")

        if response.status == 200:
            events = json.loads(data)
            logging.info("Resposta recebida com sucesso")
            return events
        else:
            logging.error(f"Erro na resposta: {response.status}")
            return {"error": f"Erro: {response.status}"}
    except Exception as e:
        logging.error(f"Exceção ao fazer a requisição: {str(e)}")
        return {"error": str(e)}
    finally:
        conn.close()

def cross_reference_events(events):
    combined_events = {}

    if "odds" in events:
        for odd in events["odds"]:
            event_id = odd["event_id"]
            if event_id not in combined_events:
                combined_events[event_id] = {"odds": odd, "scores": None}

    if "scores" in events:
        for score in events["scores"]:
            event_id = score["event_id"]
            if event_id in combined_events:
                combined_events[event_id]["scores"] = score
            else:
                combined_events[event_id] = {"odds": None, "scores": score}

    return combined_events

def format_live_events(combined_events):
    formatted_data = []

    for event_id, event_data in combined_events.items():
        odds = event_data["odds"]
        scores = event_data["scores"]

        if odds:
            formatted_data.append(f"\nPaís: {odds['category_name']}")
            formatted_data.append(f"Campeonato: {odds['tournament_name']}")
            formatted_data.append(f"Casa: {odds['home']} vs Fora: {odds['away']}")
            formatted_data.append(f"Data de Início: {odds['date_start']}")
        if scores:
            formatted_data.append(f"Placar Casa: {scores['home_score']} vs Placar Fora: {scores['away_score']}")
            formatted_data.append(f"Tempo de Jogo: {scores['match_time']}")
            formatted_data.append(f"Escanteios Casa: {scores['home_corners']} vs Escanteios Fora: {scores['away_corners']}")
            formatted_data.append(f"Cartões Amarelos Casa: {scores['home_yellow_cards']} vs Cartões Amarelos Fora: {scores['away_yellow_cards']}")
            formatted_data.append(f"Cartões Vermelhos Casa: {scores['home_red_cards']} vs Cartões Vermelhos Fora: {scores['away_red_cards']}")

    return "\n".join(formatted_data)

def check_for_score_updates(interval=30):
    previous_scores = {}
    first_run = True

    while True:
        logging.info("Verificando atualizações de placar")
        events = get_live_events()
        if "error" in events:
            logging.error(events["error"])
        else:
            combined_events = cross_reference_events(events)

            if first_run:
                logging.info("Exibindo todos os resultados na primeira execução")
                formatted_events = format_live_events(combined_events)
                print(formatted_events)
                first_run = False

            for event_id, event_data in combined_events.items():
                odds = event_data["odds"]
                scores = event_data["scores"]

                if scores:
                    home_score = scores["home_score"]
                    away_score = scores["away_score"]
                    if event_id not in previous_scores:
                        previous_scores[event_id] = {"home_score": home_score, "away_score": away_score}
                    else:
                        prev_home_score = previous_scores[event_id]["home_score"]
                        prev_away_score = previous_scores[event_id]["away_score"]
                        if home_score != prev_home_score or away_score != prev_away_score:
                            previous_scores[event_id] = {"home_score": home_score, "away_score": away_score}
                            logging.info(f"Gol em {odds['home']} vs {odds['away']}:")
                            logging.info(f"Novo placar - Casa: {home_score}, Fora: {away_score}")
                            logging.info(f"Data de Início: {odds['date_start']}")
                            logging.info(f"Categoria: {odds['category_name']}")
                            logging.info(f"Torneio: {odds['tournament_name']}")

        time.sleep(interval)

if __name__ == "__main__":
    check_for_score_updates()
