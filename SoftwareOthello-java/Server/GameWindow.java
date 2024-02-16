import javax.swing.JFrame;
import javax.swing.event.MenuDragMouseEvent;
import javax.swing.event.MouseInputAdapter;
import java.awt.event.MouseEvent;

import java.awt.*;
import javax.swing.*;

public class GameWindow extends JFrame {
    BoardPanel board;
    boolean isAbleToClick;      // ゲーム終了時はクリック入力を拒否する
    ManageBoard boardManager;
    int x, y;                   // ウィンドウ内におけるクリック位置の座標

    GameWindow(String title, ManageBoard boardManager) {
        this.boardManager = boardManager;

        // マスターフレーム設定
        setTitle(title);
        setResizable(false);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);

        // 盤面フレーム設定
        board = new BoardPanel(560, 560, boardManager);
        getContentPane().setLayout(new FlowLayout());
        board.addMouseListener(new MouseCheck());
        getContentPane().add(board);
        pack();

        isAbleToClick = false;
    }

    // 盤面のクリックイベント処理
    private class MouseCheck extends MouseInputAdapter {
        @Override
        public void mousePressed(MouseEvent e) {
            if(isAbleToClick) {
                x = e.getX();
                y = e.getY();
                // ウィンドウのうちオセロ盤面上の部分がクリックされた場合
                if(x>=board.xLowerLimit && x<=board.xUpperLimit && y>=board.yLowerLimit && y<=board.yUpperLimit) {
                    board.getPosition(x, y);
                    boardManager.checkBoard(board.xValue, board.yValue);
                }
            }
        }
    }
}
