import chess
import chess.pgn 
import random

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def evaluate_board(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -99999  # Black wins
        else:
            return 99999   # White wins
            
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = PIECE_VALUES[piece.piece_type]
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score

def minimax(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if is_maximizing:
        max_score = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # There's a better move already, no need to continue
        return max_score
    else:
        min_score = float('inf')
        for move in board.legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_score = min(min_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break  # There's a better move already, no need to continue
        return min_score

def get_bot_move(board, depth=3):
    legal_moves = list(board.legal_moves)
    best_move = None
    random.shuffle(legal_moves)

    alpha = float('-inf')
    beta = float('inf')
    
    if board.turn == chess.WHITE:
        best_score = float('-inf')
        for move in legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
    else:
        best_score = float('inf')
        for move in legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, score)

    return best_move

def play_game():
    board = chess.Board()
    
    # Initialize PGN Tracker
    pgn_game = chess.pgn.Game()
    pgn_game.headers["Event"] = "Alpha-Beta Chess AI"
    pgn_game.headers["Date"] = "2026.07.14"
    pgn_node = pgn_game 

    print("Welcome to Chess AI!")
    user_color_input = input("Choose your color (w for White, b for Black): ").lower().strip()
    
    if user_color_input == 'b':
        user_color = chess.BLACK
        pgn_game.headers["White"] = "Minimax Bot"
        pgn_game.headers["Black"] = "Human"
        print("You are playing as BLACK. The bot will make the first move.")
    else:
        user_color = chess.WHITE
        pgn_game.headers["White"] = "Human"
        pgn_game.headers["Black"] = "Minimax Bot"
        print("You are playing as WHITE. You make the first move.")

    while not board.is_game_over():
        print('\n')
        print(board)

        # Human Turn
        if board.turn == user_color:
            move_str = input("\nEnter your move: ")
            try:
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    board.push(move)
                    pgn_node = pgn_node.add_main_variation(move)
                else:
                    print("Illegal move, Try again!")
            except ValueError:
                print("Invalid format. Use UCI format!")
        
        # Bot Turn
        else:
            print("\nBot is thinking...")
            bot_move = get_bot_move(board, depth=3) 
            if bot_move is not None:
                board.push(bot_move)
                pgn_node = pgn_node.add_main_variation(bot_move)
                print(f"Bot played: {bot_move}")

    print('\n')
    print(board)
    print("\nGame Ended")
    pgn_game.headers["Result"] = board.result()

    print("\n" + "="*40)
    print(f"FINAL FEN SNAPSHOT:\n{board.fen()}")
    print("="*40)
    
    filename = "latest_simple_minimax_game.pgn"
    with open(filename, "w") as pgn_file:
        pgn_file.write(str(pgn_game))
    
    print(f"\nGame history exported! Saved locally to: '{filename}'")

if __name__ == "__main__":
    play_game()