#ifndef BIS_GUI_H
#define BIS_GUI_H

#include <QWidget>

namespace Ui {
class BIS_GUI;
}

class BIS_GUI : public QWidget
{
    Q_OBJECT

public:
    explicit BIS_GUI(QWidget *parent = nullptr);
    ~BIS_GUI();

private:
    Ui::BIS_GUI *ui;
};

#endif // BIS_GUI_H
