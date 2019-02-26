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

namespace SmartCityDatabase
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private MySqlConnection connection;
        private string server;
        private string port;
        private string database;
        private string uid;
        private string password;

        public void Initialize()
        {
            server = "portmap.io";
            port = "61974";
            database = "test";
            uid = "test";
            password = "123";

            string connectionString;

            connectionString =
                "SERVER=" + server + ";" +
                "PORT=" + port + ";" +
                "DATABASE=" + database + ";" +
                "UID=" + uid + ";" +
                "PASSWORD=" + password + ";";

            connection = new MySqlConnection(connectionString);
        }

        public bool openConnection()
        {
            try
            {
                this.connection.Open();
                MessageBox.Show("Uspjesno povezivanje");
                return true;
            }
            catch (MySqlException e)
            {
                MessageBox.Show("Neuspjelo povezivanje.");
                return false;
            }
        }

        public bool closeConnection()
        {
            try
            {
                connection.Close();
                return true;
            }
            catch (MySqlException e)
            {
                MessageBox.Show("Greska");
                return false;
            }
        }

        private void btnPosalji_Click(object sender, EventArgs e)
        {
            string insert = "INSERT INTO test VALUES(" + txtUnos.Text + ");";
            MySqlCommand cmd = new MySqlCommand(insert, connection);

            if (openConnection() == true)
            {
                cmd.ExecuteNonQuery();
            }
            else MessageBox.Show("Neuspjelo upisivanje podataka.");
        }

        public List< string >[] Select()
        {
            string select = "SELECT * FROM test;";

            List<string>[] list = new List<string>[3];
            list[0] = new List<string>();

            if (openConnection() == true)
            {
                MySqlCommand cmd = new MySqlCommand(select, connection);
                MySqlDataReader dataReader = cmd.ExecuteReader();

                while (dataReader.Read())
                {
                    list[0].Add(dataReader["unos"] + "");
                }
                dataReader.Close();

                closeConnection();

                return list;
            }
            else
            {
                return list;
            }
        }

        private void btnPrikazi_Click(object sender, EventArgs e)
        {
            txtPrikaz.Text = Select().ToString();
        }
    }
}
