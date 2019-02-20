using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MySql.Data.MySqlClient;

namespace WindowsFormsApp1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            MySqlConnection connection;

            string server = "portmap.io";
            string port = "61974";
            string database = "parking";
            string user = "test";
            string password = "123";

            string connectionString =
                "SERVER=" + server + ";" +
                "PORT=" + port + ";" +
                "DATABASE=" + database + ";" +
                "UID=" + user + ";" +
                "PASSWORD=" + password + ";";

            connection = new MySqlConnection(connectionString);

            try
            {
                connection.Open();
                MessageBox.Show("Uspjesno povezivanje na bazu podataka.");
            }
            catch (MySqlException ex)
            {
                MessageBox.Show("Neuspjelo povezivanje na bazu.");
            }
        }
    }
}
