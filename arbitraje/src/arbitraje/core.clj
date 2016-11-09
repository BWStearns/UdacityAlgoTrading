(ns arbitraje.core
  (:require [clojure.java.io]
            [incanter.core :as ic]
            [incanter.stats :as stats])
  (:use [incanter io])
  (:gen-class))


;; DATA FETCHING


(defn data-path
  "Path to data file for a symbol"
  [sym]
  (str "./data/" sym))

(defn mk-yahoo-url
  [sym]
  (str "http://ichart.finance.yahoo.com/table.csv?s=" sym))

(defn pull-historical-data
  "Download up to date historical data from Yahoo"
  [sym]
  (spit (data-path sym)
        (slurp (mk-yahoo-url sym))))

(defn keywordize
  [word]
  (keyword (clojure.string/replace word #" " "")))

(defn keywordize-dataset
  [ds]
  (let [cols (ic/col-names ds)
        new-cols (map keywordize cols)]
    (ic/col-names ds new-cols)))

(defn get-or-fetch-data
  "Gets the dataset for a given symbol, going to Yahoo if necessary"
  [sym]
  (if (not (.exists (clojure.java.io/as-file (data-path sym))))
    (pull-historical-data sym))
  (keywordize-dataset (read-dataset (data-path sym)
                :header true
                :keyword-headers false)))

;; DATASET MANIPULATION
;; note: Maybe have a global store of loaded datasets?

(defn adj-close
  [sym]
  (-> (get-or-fetch-data sym)
      (ic/sel :cols [:Date, :AdjClose])
      (ic/col-names [:Date, (keywordize sym)])))

(defn join-by
  [lkey & rkey]
  (partial ic/$join [lkey (or rkey lkey)]))

(defn index-on-spy
  [syms]
  (reduce (join-by :Date)
          (adj-close "SPY")
          (map adj-close syms)))


(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  (println "Hello, World!"))
