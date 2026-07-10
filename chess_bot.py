import chess
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

def get_greedy_move(board):

    legal_moves = list(board.legal_moves)
    best_move = None
    random.shuffle(legal_moves) 

    if board.turn == chess.WHITE:
        best_score = float('-inf')
    else:
        best_score = float('inf')

    for move in legal_moves:
        board.push(move)
        score = evaluate_board(board)
        board.pop()
        
        if board.turn == chess.WHITE:
            if score > best_score:  # White wants to maximize
                best_score = score
                best_move = move
        else:
            if score < best_score:  # Black wants to minimize
                best_score = score
                best_move = move
            
    return best_move

def play_game():
    board = chess.Board()

    print("Welcome to Chess AI!")
    user_color_input = input("Choose your color (w for White, b for Black): ").lower().strip()
    
    if user_color_input == 'b':
        user_color = chess.BLACK
        print("You are playing as BLACK. The bot will make the first move.")
    else:
        user_color = chess.WHITE
        print("You are playing as WHITE. You make the first move.")

    while not board.is_game_over():
        print('\n')
        print(board)

        if board.turn == user_color:
            move_str = input("\nEnter your move: ")
            try:
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Illegal move, Try again!")

            except ValueError:
                print("Invalid format. Use UCI format!")
        
        else:
            print("\nBot is thinking...")
            bot_move = get_greedy_move(board)
            if bot_move is not None:
                board.push(bot_move)
                print(f"Bot played: {bot_move}")

    print('\n')
    print(board)
    print("\nGame over")
    print(f"Result: {board.result()}")

if __name__ == "__main__":
    play_game()